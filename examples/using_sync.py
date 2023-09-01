from orionx_api_client import Orionx

api_key = "API_KEY"
secret_key = "SECRET_KEY"
client = Orionx(api_key, secret_key)

with client as session:
    ds = session.dsl()

    query = ds.Query.marketStats.args(marketCode="BTCCLP", aggregation="h1").select(
        ds.MarketStatsPoint.open
    )

    print(session.execute(query))

    # marketOrderBook
    query = """
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

    params = {"marketCode": "BTCCLP"}

    operation_name = "getOrderBook"

    print(session.execute(query, variable_values=params))
