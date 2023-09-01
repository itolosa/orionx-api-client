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
    def __init__(self, future: concurrent.futures.Future):
        self.future = future
        self._data = None
        self._errors = None
        self._extensions = None
        self.filled = False

    def _lazy_load(self):
        if not self.filled:
            result = self.future.result()
            self._errors = result.get("errors")
            self._data = result.get("data")
            self._extensions = result.get("extensions")
            self.filled = True

    @property
    def data(self):
        self._lazy_load()
        return self._data

    @property
    def errors(self):
        self._lazy_load()
        return self._errors

    @property
    def extensions(self):
        self._lazy_load()
        return self._extensions


class OrionxBatchTransport(RequestsHTTPTransport):
    """
    based on: https://dev-blog.apollodata.com/query-batching-in-apollo-63acfd859862
    """

    class TerminateBatcher(Exception):
        pass

    def __init__(
        self, api_key: str, secret_key: str, *args: Any, **kwargs: Any
    ) -> None:
        RequestsHTTPTransport.__init__(self, *args, **kwargs)
        self.headers_builder = HeadersBuilder(api_key, secret_key)

        self.query_batcher_queue = queue.Queue()
        self.query_batcher = threading.Thread(target=self._batch_query, daemon=True)
        self.query_batcher.start()

    def _batch_query(self) -> None:
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
        # Using the created session to perform requests
        assert self.session is not None

        return self.session.request(self.method, self.url, **post_args)  # type: ignore

    def execute(  # type: ignore
        self,
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> FutureExecResult:
        """Execute GraphQL query.

        Execute the provided document AST against the configured remote server. This
        uses the requests library to perform a HTTP POST request to the remote server.

        :param document: GraphQL query as AST Node object.
        :param variable_values: Dictionary of input parameters (Default: None).
        :param operation_name: Name of the operation that shall be executed.
            Only required in multi-operation documents (Default: None).
        :return: The result of execution.
            `data` is the result of executing the query, `errors` is null
            if no errors occurred, and is a non-empty array if an error occurred.
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
