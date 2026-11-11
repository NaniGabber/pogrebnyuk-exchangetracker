from typing import Any

import pytest
from pydantic import ValidationError

from exchangetracker.services.schemas import ExchangeRateIn


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("41.5", 41.5),
        (41.5, 41.5),
        ("unknown", None),
        (None, None),
    ],
)
def test_rate_is_parsed(
    raw: float | str | None,
    expected: float | None,
) -> None:
    payload: dict[str, Any] = {
        "asset": "USD",
        "type": "currency",
        "rate": raw,
        "date": "2026-10-08",
    }

    model = ExchangeRateIn(**payload)

    assert model.rate == expected


def test_asset_is_uppercased() -> None:
    model = ExchangeRateIn(
        asset="usd",
        type="currency",
        rate=41.5,
        date="2026-10-08",
    )

    assert model.asset == "USD"


def test_asset_spaces_are_normalized() -> None:
    model = ExchangeRateIn(
        asset="  US   D  ",
        type="currency",
        rate=41.5,
        date="2026-10-08",
    )

    assert model.asset == "US D"


def test_asset_type_spaces_are_normalized() -> None:
    model = ExchangeRateIn(
        asset="USD",
        type="  foreign   currency  ",
        rate=41.5,
        date="2026-10-08",
    )

    assert model.asset_type == "foreign currency"


def test_type_alias_is_supported() -> None:
    model = ExchangeRateIn(
        asset="USD",
        type="currency",
        rate=41.5,
        date="2026-10-08",
    )

    assert model.asset_type == "currency"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "asset": "",
            "type": "currency",
            "rate": 41.5,
            "date": "2026-10-08",
        },
        {
            "asset": "USD",
            "type": "",
            "rate": 41.5,
            "date": "2026-10-08",
        },
        {
            "asset": "USD",
            "type": "currency",
            "rate": 0,
            "date": "2026-10-08",
        },
        {
            "asset": "USD",
            "type": "currency",
            "rate": -1,
            "date": "2026-10-08",
        },
        {
            "asset": "USD",
            "type": "currency",
            "rate": 41.5,
            "date": "",
        },
    ],
)
def test_invalid_exchange_rate_is_rejected(
    payload: dict[str, Any],
) -> None:
    with pytest.raises(ValidationError):
        ExchangeRateIn(**payload)
