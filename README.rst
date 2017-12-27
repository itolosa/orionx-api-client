=================
orionx-api-client
=================

Orionx Api Client is a client library to manage operations on the Orionx exchange platform.

It can perform transactions and display market info by querying a graphql endpoint.

Installation
============

To install, use `pip`:

```bash
$ pip install --upgrade orionx-api-client
```

Python Version
==============

Python 2.7, 3.4, 3.5, and 3.6 are supported.

Example
=======
.. code:: python

    from orionxapi.client import OrionxApiClient

    # rpc_user and rpc_password are set in the bitcoin.conf file
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

For more information of methods available see `orionxapi/orionx_queries.py`
