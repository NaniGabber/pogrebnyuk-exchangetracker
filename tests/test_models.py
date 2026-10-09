import pytest

from exchangetracker.domain.models import ExchangeRate


@pytest.mark.parametrize(
    "asset, asset_type, rate, date",
    [
        (" ", "currency", 41.5, "2026-10-08"),  # порожній asset
        ("USD", " ", 41.5, "2026-10-08"),  # порожній asset_type
        ("USD", "currency", -5, "2026-10-08"),  # від'ємний курс
        ("USD", "currency", 0, "2026-10-08"),  # нульовий курс
        ("USD", "currency", 41.5, " "),  # порожня дата
    ],
)
def test_invalid_exchange_rate_rejected(
    asset: str,
    asset_type: str,
    rate: float,
    date: str,
) -> None:
    with pytest.raises(ValueError):
        ExchangeRate(asset, asset_type, rate, date)


def test_frozen_model_is_hashable() -> None:
    a = ExchangeRate("USD", "currency", 41.5, "2026-10-08")
    b = ExchangeRate("USD", "currency", 41.5, "2026-10-08")

    assert len({a, b}) == 1
