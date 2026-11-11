from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from exchangetracker.services.market_data import (
    convert_usd_to_uah,
    get_currency_rates_privat,
    get_currency_rates_yahoo,
    get_metal_prices_usd,
    get_usd_uah,
    safe_request,
)


@patch("exchangetracker.services.market_data.requests.get")
def test_safe_request_success(mock_get):
    response = Mock()
    response.json.return_value = [{"ccy": "USD"}]
    response.raise_for_status.return_value = None

    mock_get.return_value = response

    result = safe_request("https://example.com")

    assert result == [{"ccy": "USD"}]


@patch("exchangetracker.services.market_data.requests.get")
def test_safe_request_failure(mock_get):
    mock_get.side_effect = requests.RequestException

    result = safe_request("https://example.com")

    assert result == []


@patch("exchangetracker.services.market_data.safe_request")
def test_get_usd_uah(mock_request):
    get_usd_uah.cache_clear()

    mock_request.return_value = [
        {
            "ccy": "USD",
            "sale": "41.50",
        }
    ]

    assert get_usd_uah() == 41.5


@patch("exchangetracker.services.market_data.safe_request")
def test_get_usd_uah_raises(mock_request):
    get_usd_uah.cache_clear()

    mock_request.return_value = []

    with pytest.raises(
        ValueError,
        match="Не вдалося отримати курс USD/UAH",
    ):
        get_usd_uah()


@patch("exchangetracker.services.market_data.safe_request")
def test_get_currency_rates_privat(mock_request):
    mock_request.return_value = [{"ccy": "USD"}]

    result = get_currency_rates_privat()

    assert result == [{"ccy": "USD"}]


@patch("exchangetracker.services.market_data.yf.Ticker")
def test_get_currency_rates_yahoo(mock_ticker):
    history = pd.DataFrame({"Close": [1.10, 1.15]})

    ticker = Mock()
    ticker.history.return_value = history

    mock_ticker.return_value = ticker

    result = get_currency_rates_yahoo(
        "USD",
        ["EUR"],
    )

    assert result == {"EUR": 1.15}


@patch("exchangetracker.services.market_data.yf.Ticker")
def test_get_currency_rates_yahoo_skip_empty(
    mock_ticker,
):
    ticker = Mock()
    ticker.history.return_value = pd.DataFrame()

    mock_ticker.return_value = ticker

    get_currency_rates_yahoo(
        "USD",
        ["EUR"],
    )


@patch("exchangetracker.services.market_data.yf.Ticker")
def test_get_metal_prices_usd(mock_ticker):
    history = pd.DataFrame({"Close": [3000.0]})

    ticker = Mock()
    ticker.history.return_value = history

    mock_ticker.return_value = ticker

    result = get_metal_prices_usd()

    assert result
    assert result["Gold (XAU)"] == 3000.0


def test_convert_usd_to_uah():
    result = convert_usd_to_uah(
        {
            "Gold": 100.0,
            "Silver": 50.0,
        },
        40.0,
    )

    assert result == {
        "Gold": 4000.0,
        "Silver": 2000.0,
    }
