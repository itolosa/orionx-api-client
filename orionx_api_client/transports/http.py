from typing import Any, Dict, Optional

from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode
from graphql.execution import ExecutionResult

from .builders.headers import HeadersBuilder
from .builders.payload import PayloadBuilder


class OrionxHTTPTransport(RequestsHTTPTransport):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super(OrionxHTTPTransport, self).__init__(*args, **kwargs)
        self.headers_builder = HeadersBuilder(api_key, secret_key)

    def execute(
        self,
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        timeout: Optional[int] = None,
        extra_args: Optional[Dict[str, Any]] = None,
        upload_files: bool = False,
    ) -> ExecutionResult:
        headers = self.headers_builder.build(
            PayloadBuilder.build(
                document,
                variable_values,
                operation_name,
            )
        )

        return super().execute(
            document,
            variable_values,
            operation_name,
            timeout,
            {**(extra_args or {}), **{"headers": headers}},
            upload_files,
        )
