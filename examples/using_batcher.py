from orionx_api_client import Orionx, as_completed

api_key = "API_KEY"
secret_key = "SECRET_KEY"
client = Orionx(api_key, secret_key, batching=True)

with client as session:
    results = []
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

    results.append(session.execute(query, variable_values=params))

    # marketStats
    query = """
        query getMarketStats($marketCode: ID!, $aggregation: MarketStatsAggregation!) {
            marketStats(marketCode: $marketCode, aggregation: $aggregation) {
            _id
            open
            close
            high
            low
            volume
            count
            fromDate
            toDate
            __typename
            }
        }
    """

    params = {"marketCode": "BTCCLP", "aggregation": "h1"}

    operation_name = "getMarketStats"

    results.append(session.execute(query, variable_values=params))

    # market
    query = """
        query getMarketIdleData($code: ID) {
            market(code: $code) {
            code
            lastTrade {
                price
                __typename
            }
            secondaryCurrency {
                code
                units
                format
                longFormat
                __typename
            }
            __typename
            }
        }
    """

    params = {"code": "BTCCLP"}

    operation_name = "getMarketIdleData"

    results.append(session.execute(query, variable_values=params))


for result in as_completed(results):
    if result.errors:
        print("error:", result.errors[0])
    else:
        print("data:", result.data)
