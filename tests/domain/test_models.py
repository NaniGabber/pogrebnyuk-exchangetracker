from typing import Any

import pytest

from exchangetracker.services.schemas import ExchangeRateIn


def make(**overrides: object) -> ExchangeRateIn:
    data: dict[str, Any] = {
        "asset": "USD",
        "asset_type": "currency",
        "rate": 41.5,
        "date": "2026-10-08",
    }

    data.update(overrides)

    return ExchangeRateIn(**data)


@pytest.mark.parametrize(
    "overrides",
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
    overrides: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        make(**overrides)


@pytest.mark.parametrize(
    ("rate", "expected"),
    [
        (None, False),
        (10.0, False),
        (49.99, False),
        (50.0, True),
        (100.0, True),
    ],
)
def test_is_high_rate(rate: float | None, expected: bool) -> None:
    assert make(rate=rate).is_high_rate is expected
