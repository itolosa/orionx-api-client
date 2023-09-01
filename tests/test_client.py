import logging
import os
from unittest.mock import MagicMock

import pytest
import requests
from dotenv import load_dotenv
from gql.dsl import DSLField, DSLSchema
from gql.transport.exceptions import (
    TransportClosed,
    TransportProtocolError,
    TransportServerError,
)
from graphql import ExecutionResult
from pytest_mock import MockerFixture

from orionx_api_client import Orionx
from orionx_api_client.client import as_completed

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
        batching=True,
    )


@pytest.fixture
def sync_client(api_key: str, secret_key: str) -> Orionx:
    return Orionx(
        api_key=api_key,
        secret_key=secret_key,
    )


def build_query(ds: DSLSchema) -> DSLField:
    return ds.Query.marketOrderBook.args(marketCode="BTCCLP", limit=50).select(
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


def test_using_batching_using_dsl(caplog, batch_client: Orionx) -> None:
    caplog.set_level(logging.INFO)
    with batch_client as session:
        query = build_query(session.dsl())
        result = session.execute(query)
        assert isinstance(result, ExecutionResult)
        assert isinstance(result.__repr__(), str)


def test_sync_using_string(sync_client: Orionx) -> None:
    with sync_client as session:
        q = """
            query getOrderBook($marketCode: ID!) {
                orderBook: marketOrderBook(marketCode: $marketCode, limit: 50) {
                    buy {
                        limitPrice
                        amount
                    }
                    sell {
                        limitPrice
                        amount
                    }
                    spread
                }
            }
        """
        session.execute(q, variable_values={"marketCode": "BTCCLP", "limit": 50})


def test_validate_should_not_raise_using_dsl(sync_client: Orionx) -> None:
    with sync_client as session:
        q = build_query(session.dsl())
        session.validate(q)


def test_as_completed(batch_client: Orionx) -> None:
    with batch_client as session:
        results = []

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

        results.append(session.execute(query, variable_values={"marketCode": "BTCCLP"}))

        # marketStats
        query = """
            query getMarketStats(
                $marketCode: ID!,
                $aggregation: MarketStatsAggregation!) {
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

        results.append(
            session.execute(
                query, variable_values={"marketCode": "BTCCLP", "aggregation": "h1"}
            )
        )

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

        results.append(
            session.execute(
                query,
                variable_values={"code": "BTCCLP"},
                operation_name="getMarketIdleData",
            )
        )

        for result in as_completed(results):
            assert isinstance(result.data, dict)
            assert result.errors is None


def test_when_no_wait_to_complete_batching(batch_client: Orionx) -> None:
    with batch_client as session:
        results = []

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

        results.append(session.execute(query, variable_values={"marketCode": "BTCCLP"}))

        # marketStats
        query = """
            query getMarketStats(
                $marketCode: ID!,
                $aggregation: MarketStatsAggregation!) {
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

        results.append(
            session.execute(
                query, variable_values={"marketCode": "BTCCLP", "aggregation": "h1"}
            )
        )

    for result in as_completed(results):
        try:
            result.errors
            raise Exception("This should not happen")
        except TransportClosed:
            pass


def test_sync_using_dsl(sync_client: Orionx) -> None:
    with sync_client as session:
        query = build_query(session.dsl())
        assert isinstance(session.execute(query), dict)


def test_http_error(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 400
        response_mock.json.side_effect = requests.HTTPError(
            "An Exception", response=response_mock
        )
        response_mock.raise_for_status.side_effect = requests.HTTPError(
            "An Exception", response=response_mock
        )
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportServerError:
            pass


def test_no_json_response(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 400
        response_mock.json.side_effect = Exception("An Exception")
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportProtocolError:
            pass


def test_json_has_no_keys(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = [{}]
        response_mock.text = "[{}]"
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportProtocolError:
            pass


def test_no_list_response(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {}
        response_mock.text = "{}"
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportProtocolError:
            pass


def test_list_mismatch_length(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = []
        response_mock.text = "[]"
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportProtocolError:
            pass


def test_list_with_invalid_content(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
        mock: MagicMock = mocker.patch(
            "orionx_api_client.client.OrionxBatchTransport._request"
        )
        response_mock = MagicMock(spec=requests.Response)
        response_mock.headers = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = "[[]]"
        response_mock.text = "[[]]"
        mock.return_value = response_mock

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

        result = session.execute(query, variable_values={"marketCode": "BTCCLP"})

        try:
            assert isinstance(result, ExecutionResult)
            assert result.errors is None
            raise Exception("This should not happen")
        except TransportProtocolError:
            pass


def test_closed_session(mocker: MockerFixture, batch_client: Orionx) -> None:
    with batch_client as session:
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

    try:
        session.execute(query, variable_values={"marketCode": "BTCCLP"})
        raise Exception("This should not happen")
    except TransportClosed:
        pass
