import concurrent.futures
import typing
from typing import Any, Dict, Iterable, Iterator, Optional, Union

from gql import Client, gql
from gql.client import SyncClientSession
from gql.dsl import DSLField, DSLQuery, DSLSchema, dsl_gql
from graphql import ExecutionResult

from .constants import Constants
from .transports.batch import FutureExecResult, OrionxBatchTransport
from .transports.http import OrionxHTTPTransport


class SyncClientSessionDecorator:
    """
    A decorator class for synchronous client sessions.

    This class provides methods to work with gql's SyncClientSession
    and offers additional functionality like query validation and DSL support.
    """

    def __init__(self, session: SyncClientSession, batching: bool = False) -> None:
        """
        Initialize the SyncClientSessionDecorator.

        Args:
            session: The synchronous client session to be decorated.
            batching: A flag indicating if batching should be used. Default is False.
        """
        self.session = session
        self.batching = batching

    def dsl(self) -> DSLSchema:
        """
        Retrieve the DSL schema.

        Asserts that the client's schema is not None and then returns the DSLSchema.

        Returns:
            The DSLSchema associated with the client's schema.
        
        Raises:
            AssertionError: If the client's schema is None.
        """
        assert self.session.client.schema is not None
        return DSLSchema(self.session.client.schema)

    def validate(self, query: DSLField) -> None:
        """
        Validate a given query against the schema.

        Args:
            query: The query (as DSLField) to be validated.

        Returns:
            None. 

        Raises:
            AssertionError: If the validation fails.
        """
        document = dsl_gql(DSLQuery(query))
        return self.session.client.validate(document)

    def execute(
        self,
        query: Union[DSLField, str],
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], ExecutionResult]:
        """
        Execute a query.

        Args:
            query: The query to be executed.
            variable_values: The variable values for the query. Default is None.
            operation_name: The operation name. Default is None.
            **kwargs: Additional arguments passed directly to gql's `session.execute`.

        Returns:
            The execution result.
        """
        if isinstance(query, str):
            document = gql(query)
        else:
            document = dsl_gql(DSLQuery(query))

        if self.batching:
            return self.session._execute(
                document,
                variable_values,
                operation_name,
                **kwargs,
            )
        else:
            return self.session.execute(
                document,
                variable_values,
                operation_name,
                **kwargs,
            )



class Orionx:
    """
    A client for interacting with the Orionx API.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        url: Optional[str] = None,
        batching: bool = False,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Orionx client.

        Args:
            api_key: The API key used for authentication.
            secret_key: The secret key used for authentication.
            url: The base URL for the API. If not provided, \
                the default from `Constants.API_URL_V2` is used.
            batching: If set to True, the OrionxBatchTransport is used. \
                Otherwise, OrionxHTTPTransport is used.
            timeout: Timeout for the request in seconds. If None, there's no limit.
            **kwargs: Arbitrary keyword arguments. \
                These are passed directly to the gql Client.
        """
        if batching:
            TransportKlass = OrionxBatchTransport
        else:
            TransportKlass = OrionxHTTPTransport

        self.batching = batching

        transport = TransportKlass(
            api_key,
            secret_key,
            url=url or Constants.API_URL_V2,
            use_json=True,
            timeout=timeout,
        )
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
            **kwargs,
        )

    def __enter__(self):
        return SyncClientSessionDecorator(
            typing.cast(SyncClientSession, self.client.connect_sync()),
            batching=self.batching,
        )

    def __exit__(self, *args):
        self.client.close_sync()


def as_completed(
    exec_results: Iterable[FutureExecResult],
    timeout: Optional[float] = None,
) -> Iterator[FutureExecResult]:
    """
    Get completed execution results.

    Args:
        exec_results: A list of FutureExecResult.
        timeout: Maximum number of seconds to wait. \
            If None, then there's no limit.

    Returns:
        An iterator over completed execution results.
    """
    future_to_exres = {e.future: e for e in exec_results}
    for future in concurrent.futures.as_completed(future_to_exres, timeout):
        exec_result = future_to_exres[future]
        yield exec_result
