=================
orionx-api-client
=================


Orionx Api Client es un cliente que permite manejar operaciones en la plataforma de exchange orionx.io

Permite realizar transacciones y mostrar informacion del mercado consultando un endpoint con graphql

|pypi|

Instalación
============

Para instalar, usar ``pip``:

.. code:: bash

    $ pip install --upgrade orionx-api-client


Versiones
=========

La librería soporta Python 2.7, 3.4, 3.5, y 3.6.


Ejemplo
=======

.. code:: python

    # This file is located at: examples/using_manager.py

    from orionxapi import client
    from pygql import gql
    from pygql.dsl import DSLSchema

    api_key = 'API_KEY'
    secret_key = 'SECRET_KEY'
    client = client(api_key, secret_key)

    ds = DSLSchema(client)

    query_dsl = ds.Query.marketStats.args(
                    marketCode="CHACLP", 
                    aggregation="h1"
                  ).select(ds.MarketStatsPoint.open)

    print(ds.query(query_dsl))

    # marketOrderBook
    query = gql('''
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
    ''')

    params = {
      "marketCode": "CHACLP"
    }

    operation_name = "getOrderBook"

    print(client.execute(query, variable_values=params))

* Para ejecutar ``mutations`` usar: ``ds.mutation(query_dsl)`` 
* Para ejecutar ``queries`` usar: ``ds.query(query_dsl)`` 
* Se pueden usar diccionarios en los argumentos para especificar objetos
* La funcionalidad de DSL es lograda gracias a ``gql`` (https://github.com/itolosa/pygql)

Query Batching
==============

Es posible acelerar las consultas realizándolas simultaneamente usando el parametro ``use_batching=True``:

.. code:: python

    from orionxapi import client, as_completed
    from pygql import gql
    from pygql.dsl import DSLSchema
    
    api_key = 'API_KEY'
    secret_key = 'SECRET_KEY'

    client = client(api_key, secret_key, use_batching=True)

    ds = DSLSchema(client)
    
    query = gql('''
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
    ''')

    params = {
      "marketCode": "CHACLP"
    }

    operation_name = "getOrderBook"

    print(client.execute(query, variable_values=params).data)


Para más detalles véase ``examples/using_batcher.py``


Implementación basada en: https://dev-blog.apollodata.com/query-batching-in-apollo-63acfd859862

.. |pypi| image:: https://badge.fury.io/py/orionx-api-client.svg
   :target: https://badge.fury.io/py/orionx-api-client
