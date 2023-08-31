import os

import pytest
from dotenv import load_dotenv
from gql.dsl import DSLField, DSLSchema

from orionx_api_client.client import Orionx

load_dotenv()


@pytest.fixture
def api_key() -> str:
    return os.environ["api_key"]


@pytest.fixture
def secret_key() -> str:
    return os.environ["secret_key"]


@pytest.fixture
def batch_client(api_key: str, secret_key: str) -> Orionx:
    return Orionx(
        api_key=api_key,
        secret_key=secret_key,
        use_batching=True,
    )


@pytest.fixture
def sync_client(api_key: str, secret_key: str) -> Orionx:
    return Orionx(
        api_key=api_key,
        secret_key=secret_key,
    )


def build_query(ds: DSLSchema) -> DSLField:
    return ds.Query.marketOrderBook.args(marketCode="CHACLP", limit=50).select(
        ds.MarketOrderBook.buy.select(
            ds.MarketBookOrder.limitPrice,
            ds.MarketBookOrder.amount,
        ),
        ds.MarketOrderBook.sell.select(
            ds.MarketBookOrder.limitPrice,
            ds.MarketBookOrder.amount,
        ),
        ds.MarketOrderBook.spread,
    )


@pytest.mark.vcr
def test_using_batching_using_dsl(batch_client: Orionx) -> None:
    with batch_client as session:
        query = build_query(session.dsl())

        print(session.execute(query))


@pytest.mark.vcr
def test_without_batching_using_dsl(sync_client: Orionx) -> None:
    with sync_client as session:
        query = build_query(session.dsl())

        print(session.execute(query))
