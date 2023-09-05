import concurrent.futures
import json
import logging
import queue
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from gql.transport.exceptions import (
    TransportClosed,
    TransportProtocolError,
    TransportServerError,
)
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode, ExecutionResult

from .builders.headers import HeadersBuilder
from .builders.payload import PayloadBuilder

log = logging.getLogger(__name__)


class FutureExecResult(ExecutionResult):
    """
    Extension of the ExecutionResult class for \
        handling execution results retrieved asynchronously.

    This class utilizes the future mechanism to \
        lazily fetch the data when the future result is available.
    """

    def __init__(self, future: concurrent.futures.Future):
        """
        Initialize the FutureExecResult instance.

        Args:
            future: A future instance containing the eventual execution result.
        """
        self.future = future
        self._data = None
        self._errors = None
        self._extensions = None
        self.filled = False

    def _lazy_load(self) -> None:
        """
        Internal method to load the result from the future when it's ready.
        """
        if not self.filled:
            result = self.future.result()
            self._errors = result.get("errors")
            self._data = result.get("data")
            self._extensions = result.get("extensions")
            self.filled = True

    @property
    def data(self):
        """
        Get the data attribute, loading from the future if necessary.

        Returns:
            Data retrieved from the execution result.
        """
        self._lazy_load()
        return self._data

    @property
    def errors(self):
        """
        Get the errors attribute, loading from the future if necessary.

        Returns:
            Errors retrieved from the execution result.
        """
        self._lazy_load()
        return self._errors

    @property
    def extensions(self):
        """
        Get the extensions attribute, loading from the future if necessary.

        Returns:
            Extensions retrieved from the execution result.
        """
        self._lazy_load()
        return self._extensions


class OrionxBatchTransport(RequestsHTTPTransport):
    """
    A transport layer that supports batching of multiple
    GraphQL queries into a single HTTP request,
    based on the concepts outlined in the 
    Apollo's query batching article.

    Raises:
        TransportClosed: If the transport connection is not established.
        TransportServerError: For server-side errors during the request.
        TransportProtocolError: For invalid server responses.
    """

    class TerminateBatcher(Exception):
        """
        An internal exception class used to signal the termination of the batcher.
        """
        pass

    def __init__(
        self, api_key: str, secret_key: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the OrionxBatchTransport instance.

        Args:
            api_key: The API key for authentication.
            secret_key: The secret key for authentication.
            *args: Additional positional arguments for the \
                RequestsHTTPTransport initialization.
            **kwargs: Additional keyword arguments for the \
                RequestsHTTPTransport initialization.
        """
        RequestsHTTPTransport.__init__(self, *args, **kwargs)
        self.headers_builder = HeadersBuilder(api_key, secret_key)

        self.query_batcher_queue = queue.Queue()
        self.query_batcher = threading.Thread(target=self._batch_query, daemon=True)
        self.query_batcher.start()

    def _batch_query(self) -> None:
        """
        Continuously checks the query batcher queue,
         collecting GraphQL queries and sending them as batched requests. 

        Summary:
            - **Accumulates** multiple GraphQL queries from a queue \
                within a 10ms window.
            - Forms a single **batched request** with necessary headers and parameters.
            - **Dispatches** the batched request to the server.
            - On response, **distributes** individual results to their\
                  respective 'promise-like' `Future` objects.
            - Captures and attaches **errors** to the respective `Future`\
                  rather than raising them.

        Side Effects:
            This method's main output is the resolution or rejection of the `Future`
             objects representing each query's result. Designed to run continuously,
              making it ideal for a dedicated thread.
        """

        while True:
            payloads_and_futures: List[Tuple[dict, concurrent.futures.Future]] = []
            payload_and_future: Tuple[
                dict, concurrent.futures.Future
            ] = self.query_batcher_queue.get()

            payloads_and_futures.append(payload_and_future)

            # wait 10 ms
            time.sleep(0.01)

            while not self.query_batcher_queue.empty():
                payload_and_future = self.query_batcher_queue.get()
                payloads_and_futures.append(payload_and_future)

            payloads_and_futures = [
                (payload, future)
                for payload, future in payloads_and_futures
                if future.set_running_or_notify_cancel()
            ]

            payloads = [payload for payload, _ in payloads_and_futures]
            futures = [futures for _, futures in payloads_and_futures]

            data_key = "json" if self.use_json else "data"

            post_args = {
                "headers": self.headers_builder.build(payloads),
                "auth": self.auth,
                "cookies": self.cookies,
                "timeout": self.default_timeout,
                "verify": self.verify,
            }

            post_args[data_key] = payloads
            # Pass kwargs to requests post method
            post_args.update(self.kwargs)

            if not self.session:
                exc = TransportClosed("Transport is not connected")
                for future in futures:
                    future.set_exception(exc)
                continue

            # Using the created session to perform requests
            response = self._request(**post_args)  # type: ignore
            self.response_headers = response.headers

            def get_response_error(resp: requests.Response, reason: str) -> Exception:
                # We raise a TransportServerError if the status code
                # is 400 or higher.
                # We raise a TransportProtocolError in the other cases

                try:
                    # Raise a HTTPError if response status is 400 or higher
                    resp.raise_for_status()
                except requests.HTTPError as e:
                    exc = TransportServerError(str(e), e.response.status_code)
                    exc.__cause__ = e
                    return exc

                result_text = resp.text
                return TransportProtocolError(
                    f"Server did not return a GraphQL result: "
                    f"{reason}: "
                    f"{result_text}"
                )

            try:
                results = response.json()

                assert isinstance(results, list)
                assert len(results) == len(payloads)

                for item in results:
                    assert isinstance(item, dict)

                if log.isEnabledFor(logging.INFO):
                    log.info("<<< %s", response.text)

            except Exception:
                exc = get_response_error(response, "Not a JSON answer")
                for future in futures:
                    future.set_exception(exc)

                continue

            for result, future in zip(results, futures):
                if "errors" not in result and "data" not in result:
                    exc = get_response_error(
                        response, 'No "data" or "errors" keys in answer'
                    )
                    future.set_exception(exc)
                else:
                    future.set_result(result)

    def _request(self, **post_args: Any) -> requests.Response:
        """
        Internal method to use the established session to perform the request.

        Args:
            **post_args: Keyword arguments to be passed to the request method.

        Returns:
            The response object from the request.

        Raises:
            AssertionError: If the session is not initialized.
        """
        assert self.session is not None
        return self.session.request(self.method, self.url, **post_args)

    def execute(self, document: DocumentNode,
                variable_values: Optional[Dict[str, Any]] = None,
                operation_name: Optional[str] = None,) -> FutureExecResult:
        """
        Execute a GraphQL query, batching it if possible.

        Args:
            document: GraphQL query as an AST Node object.
            variable_values: Dictionary of input parameters (Default: None).
            operation_name: Name of the operation to be executed. \
                Required if document has multiple operations (Default: None).

        Returns:
            A FutureExecResult instance containing the eventual execution result.

        Raises:
            TransportClosed: If the transport connection is not established.
        """
        if not self.session:
            raise TransportClosed("Transport is not connected")

        payload = PayloadBuilder.build(document, variable_values, operation_name)

        # Log the payload
        if log.isEnabledFor(logging.INFO):
            log.info(">>> %s", json.dumps(payload))

        future = concurrent.futures.Future()
        self.query_batcher_queue.put((payload, future))

        return FutureExecResult(future=future)
