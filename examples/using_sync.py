from gql import gql
from gql.dsl import DSLQuery, DSLSchema, dsl_gql

from orionx_api_client import client

api_key = "API_KEY"
secret_key = "SECRET_KEY"
client = client(api_key, secret_key)

with client as session:
    assert client.schema is not None

    ds = DSLSchema(client.schema)

    query = dsl_gql(
        DSLQuery(
            ds.Query.marketStats.args(marketCode="CHACLP", aggregation="h1").select(
                ds.MarketStatsPoint.open
            )
        )
    )

    print(session.execute(query))

    # marketOrderBook
    query = gql(
        """
        query getOrderBook($marketCode: ID!) {
            orderBook: marketOrderBook(marketCode: $marketCode, limit: 50) {
            buy {
                limitPrice
                amount
                __typename
            }
            sell {
                limitPrice
                amount
                __typename
            }
            spread
            __typename
            }
        }
    """
    )

    params = {"marketCode": "CHACLP"}

    operation_name = "getOrderBook"

    print(session.execute(query, variable_values=params))
