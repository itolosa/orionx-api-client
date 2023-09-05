from typing import Any, Dict, Optional

from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode
from graphql.execution import ExecutionResult

from .builders.headers import HeadersBuilder
from .builders.payload import PayloadBuilder


class OrionxHTTPTransport(RequestsHTTPTransport):
    """
    An HTTP transport implementation for the Orionx
    platform that extends the base RequestsHTTPTransport.
    
    This class provides custom headers using the `HeadersBuilder`
    for authentication and other purposes while making requests
    to the Orionx platform.
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the OrionxHTTPTransport.

        Args:
            api_key: The API key used for authentication.
            secret_key: The secret key used for authentication.
            *args: Variable length argument list passed to the parent class.
            **kwargs: Arbitrary keyword arguments passed to the parent class.
        """
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
        """
        Execute a query with the given parameters.

        Args:
            document: The GraphQL document containing queries/mutations to be executed.
            variable_values: Variables for the GraphQL query. Default is None.
            operation_name: The operation name in the GraphQL document to be executed.
                Default is None.
            timeout: Maximum time to wait for the request to complete.
                Default is None.
            extra_args: Additional arguments to be passed for the execution.
                Default is None.
            upload_files: Flag to indicate if files need to be uploaded
                as part of the request. Default is False.

        Returns:
            The result of the GraphQL query execution.
        """
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
