from exchangetracker.domain.models import ExchangeRate

from .models import ExchangeRateORM


def _to_row(rate: ExchangeRate) -> dict[str, object]:
    return {
        "asset": rate.asset,
        "asset_type": rate.asset_type,
        "rate": rate.rate,
        "date": rate.date,
    }


def _to_domain(row: ExchangeRateORM) -> ExchangeRate:
    return ExchangeRate(
        asset=row.asset,
        asset_type=row.asset_type,
        rate=row.rate,
        date=row.date,
    )
