from typing import Any, Dict, Optional

from graphql import DocumentNode
from graphql.language.printer import print_ast


class PayloadBuilder:
    @staticmethod
    def build(
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        query_str = print_ast(document)
        payload: Dict[str, Any] = {"query": query_str}

        if operation_name:
            payload["operationName"] = operation_name

        if variable_values:
            payload["variables"] = variable_values

        return payload
