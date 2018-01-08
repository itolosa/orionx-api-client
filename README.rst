=================
orionx-api-client
=================


Orionx Api Client es un cliente que permite manejar operaciones en la plataforma de exchange orionx.io

Permite realizar transacciones y mostrar informacion del mercado consultando un endpoint con graphql

*Deprecado*: Como conectar usando headers: https://gist.github.com/itolosa/c790543f282d22f99dfc4c112e471c5a

Se recomienda usar *connection manager*

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

El siguiente ejemplo usa ``connection_manager``. Esta utilidad permite conectarse con orionx.io y comenzar a realizar peticiones solo ingresando el email, password y codigo de verificación a traves de la linea de comandos al momento de ejecutar la función ``client`` o ``orionxapi_builder``, los cuales retornan instancias de ``gql.Client`` y ``OrionxApiClient`` respectivamente, con sus parametros de conexión ya inicializados.

Los parámetros ``headers_filename`` y ``cookies_filename`` corresponden a las rutas de los archivos caché utilizados para guardar los parametros de conexión del cliente mientras estos no hayan expirado. Al especificar las rutas, deben existir los directorios previos, pero no es necesario la existencia de los archivos, es decir, en el ejemplo debe existir el directorio ``cache`` y los archivos headers.json y cookies.json se crearán automáticamente con la información necesaria una vez realizada la primera conexión.

.. code:: python

    # This file is located at: examples/using_manager.py

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


* Para ejecutar ``mutations`` usar: ``ds.mutation(query_dsl)`` 
* Para ejecutar ``queries`` usar: ``ds.query(query_dsl)`` 
* Se pueden usar diccionarios en los argumentos para especificar objetos, como ocurre con el argumento ``password`` en la consulta ``loginWithPassword`` usada en ``orionxapi/connection_manager.py``

* La funcionalidad de DSL es lograda gracias a ``gql`` (https://github.com/graphql-python/gql)
* Véase como referencia: https://github.com/graphql-python/gql/blo

Es posible configurar los parametros de conexión manualmente. Para esto se puede usar la clase ``OrionxApiClient`` como se muestra en el siguiente ejemplo. Nota: Véase instrucciones de como obtener los headers en la sección: Dónde encontrar los headers.

b/master/tests/starwars/test_dsl.py

.. code:: python

    # This file is located at: examples/legacy_api.py

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


Para más información acerca de las consultas disponibles, véase: ``orionxapi/queries.py``


Dónde encontrar los headers?
============================

Iniciar sesión dentro de orionx.io, luego en el navegador de preferencia (válido para Chrome y Firefox), abrir las Herramientas de desarrollador (Developer Tools). Luego ir a la pestaña ``Red`` o ``Network`` y hacer clic sobre una petición realizada a graphql con código 200. En **Request Headers** se podran encontrar cada uno de los parámetros necesarios. Mantener estos datos en un lugar seguro. Se puede sobreescribir cualquier header pasando valores al parametro de inicialización ``additional_headers`` de la clase ``OrionxApiClient``.

.. |pypi| image:: https://badge.fury.io/py/orionx-api-client.svg
   :target: https://badge.fury.io/py/orionx-api-client
