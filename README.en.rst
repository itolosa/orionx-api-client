=================
orionx-api-client
=================

Orionx Api Client is a client library to manage operations on the Orionx exchange platform.

It can perform transactions and display market info by querying a graphql endpoint.

*Deprecated*: How to connect with headers: https://gist.github.com/itolosa/c790543f282d22f99dfc4c112e471c5a

You should use *connection manager*

|pypi|

Installation
============

To install, use ``pip``:

.. code:: bash

    $ pip install --upgrade orionx-api-client


Python Version
==============

Python 2.7, 3.4, 3.5, and 3.6 are supported.

Example
=======
.. code:: python

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


For more information about available methods see ``orionxapi/queries.py``

Connection Manager
==================

By using this utility you can login into orionx and start making requests with just your email, password and verification code.

.. code:: python

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

* To execute mutations use: ``ds.mutation(query_dsl)`` 
* To execute queries use: ``ds.query(query_dsl)`` 
* You can use dictionaries on parameters to specify objects like ``password`` parameter on ``loginWithPassword`` query used on ``orionxapi/connection_manager.py``

* This DSL feature is achieved by using ``gql`` (https://github.com/graphql-python/gql)
* See: https://github.com/graphql-python/gql/blob/master/tests/starwars/test_dsl.py


Where do I find headers?
========================
Login into orionx.io, then on your favorite browser (valid for Chrome and Firefox) open Developers Tools or similar. Then go into ``Network`` tab and click over a graphql request with 200 status. Under **Request Headers** you may find each one of the values. Keep those values secure. You can override any header by passing a value to ``additional_headers`` initializer parameter.

NOTE
====
With the latest platform update, now you need to specify all the browser requests headers into this API. ;(

.. |pypi| image:: https://badge.fury.io/py/orionx-api-client.svg
   :target: https://badge.fury.io/py/orionx-api-client
