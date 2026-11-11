from exchangetracker.domain.models import ExchangeRate


def _to_row(rate: ExchangeRate) -> dict[str, object]:
    return {
        "asset": rate.asset,
        "asset_type": rate.asset_type,
        "rate": rate.rate,
        "date": rate.date,
    }
