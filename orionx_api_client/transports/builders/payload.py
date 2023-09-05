from typing import Any, Dict, Optional

from graphql import DocumentNode
from graphql.language.printer import print_ast


class PayloadBuilder:
    """
    A utility class for constructing GraphQL payloads.
    """

    @staticmethod
    def build(
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Construct a GraphQL payload based on the provided document and optional values.

        Args:
            document: The GraphQL document containing queries/mutations.
            variable_values: Variables for the GraphQL query. Default is None.
            operation_name: The operation name in the GraphQL \
                document to be executed. Default is None.

        Returns:
            A dictionary representing the constructed GraphQL payload.
        """
        query_str = print_ast(document)
        payload: Dict[str, Any] = {"query": query_str}

        if operation_name:
            payload["operationName"] = operation_name

        if variable_values:
            payload["variables"] = variable_values

        return payload
