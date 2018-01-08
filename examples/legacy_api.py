from orionxapi.client import OrionxApiClient

# handler initialization with custom headers
orionx_client = OrionxApiClient(additional_headers={
                                'login-token': '<your-login-token-here>',
                                'fingerprint': '<fingerprint-here>'})
my_info = orionx_client.execute_query('getMe')()
cha_stats = orionx_client.execute_query('getMarketStats')(marketCode="CHACLP")
print(my_info, cha_stats)

# bulk query support : send many queries in one single request:
# (register each query beforehand)
orionx_client.register_query('getMarketStats')(marketCode="CHACLP")
orionx_client.register_query('myOrders')(marketCode="CHACLP")
orionx_client.register_query('getMarketMid')(marketCode="CHACLP")
results = orionx_client.perform_queries()
print(results)