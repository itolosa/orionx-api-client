from orionxapi.connection_manager import client, orionxapi_builder
from orionxapi.lib.dsl import DSLSchema

# handler initialization with custom headers
client = client(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')

ds = DSLSchema(client)

query_dsl = ds.Query.marketStats.args(
                marketCode="CHACLP",
                aggregation="h1"
              ).select(ds.MarketStatsPoint.open)

print(ds.query(query_dsl))

# or using old API
orionx_client = orionxapi_builder(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')
cha_stats = orionx_client.execute_query('getMarketStats')(marketCode="CHACLP")
print(cha_stats)