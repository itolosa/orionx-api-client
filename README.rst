=================
orionx-api-client
=================

Orionx Api Client is a client library to manage operations on the Orionx exchange platform.

It can perform transactions and display market info by querying a graphql endpoint.

UPDATE. HOW TO CONNECT: https://gist.github.com/itolosa/c790543f282d22f99dfc4c112e471c5a

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

For more information of methods available see `orionxapi/orionx_queries.py`

Where do I find headers?
========================
Login into orionx.io, then on your favorite browser (valid for Chrome and Firefox) open Developers Tools or similar. Then go into `Network` tab and click over a graphql request with 200 status. Under **Request Headers** you may find each one of the values. Keep those values secure. You can override any header by passing a value to `additional_headers` initializer parameter.

.. image:: https://github.com/itolosa/orionx-api-client/raw/meta/meta/login-token-example.png
   :height: 100px
   :width: 200 px
   :scale: 50 %
   :alt: alternate text
   :align: right
NOTE
====
With the latest platform update, now you need to specify all the browser requests headers into this API. ;(
