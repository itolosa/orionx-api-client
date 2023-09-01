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
    def __init__(self, session: SyncClientSession, batching: bool = False) -> None:
        self.session = session
        self.batching = batching

    def dsl(self) -> DSLSchema:
        assert self.session.client.schema is not None
        return DSLSchema(self.session.client.schema)

    def validate(self, query: DSLField) -> None:
        document = dsl_gql(DSLQuery(query))
        return self.session.client.validate(document)

    def execute(
        self,
        query: Union[DSLField, str],
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], ExecutionResult]:
        if isinstance(query, str):
            document = gql(query)
        else:
            document = dsl_gql(DSLQuery(query))

        if self.batching:
            return self.session._execute(
                document, variable_values, operation_name, **kwargs
            )
        else:
            return self.session.execute(
                document, variable_values, operation_name, **kwargs
            )


class Orionx:
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        url: Optional[str] = None,
        batching: bool = False,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
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
    future_to_exres = {e.future: e for e in exec_results}
    for future in concurrent.futures.as_completed(future_to_exres, timeout):
        exec_result = future_to_exres[future]
        yield exec_result
