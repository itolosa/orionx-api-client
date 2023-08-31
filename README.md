# Orionx Api Client

[![PyPI version fury.io](https://badge.fury.io/py/orionx-api-client.svg)](https://pypi.python.org/pypi/orionx-api-client/) [![PyPi license](https://badgen.net/pypi/license/orionx-api-client/)](https://pypi.org/project/orionx-api-client/)
 [![PyPI pyversions](https://img.shields.io/pypi/pyversions/orionx-api-client.svg)](https://pypi.python.org/pypi/orionx-api-client/) [![Downloads](https://static.pepy.tech/badge/orionx-api-client)](https://pepy.tech/project/orionx-api-client)


Orionx Api Client is a GraphQL Client for Orionx Exchange (orionx.com)

It is able to make transactions and show market information


# Install

Using pip:

```
pip install orionx-api-client
```

Using poetry:

```
poetry add orionx-api-client
```

## Usage example

To execute the examples you have to setup an `API KEY` and a `SECRET KEY`

You can obtain them by following this tutorial: [link](https://docs.orionx.com/docs#creaci%C3%B3n-de-api-keys).

```python
from gql import gql
from gql.dsl import DSLQuery, DSLSchema, dsl_gql

from orionx_api_client import client

client = client(api_key, secret_key)

with client as session:
    assert client.schema is not None

    ds = DSLSchema(client.schema)

    query = dsl_gql(
        DSLQuery(
            ds.Query.marketStats.args(
                marketCode="CHACLP",
                aggregation="h1"
            ).select(
                ds.MarketStatsPoint.open
            )
        )
    )

    print(session.execute(query))
```

For additional details check the `examples` directory in this repository

## Query batching

You can send multiple requests at once using [query batching](https://www.apollographql.com/blog/apollo-client/performance/batching-client-graphql-queries/).

Check the file `examples/using_batcher.py` for an example.

## Contributions

You're welcome to contribute to this project! Just open a PR!
