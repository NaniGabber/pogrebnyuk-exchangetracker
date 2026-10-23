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


def test_invalid_exchange_rate_is_rejected(
    overrides: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        make(**overrides)
