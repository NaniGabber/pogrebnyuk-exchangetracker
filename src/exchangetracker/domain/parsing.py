from .models import ExchangeRate


def normalize_asset(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_rate(raw: object) -> float | None:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def to_exchange_rate(row: dict) -> ExchangeRate | None:
    asset = row.get("asset") or ""

    if not asset.strip():
        return None

    return ExchangeRate(
        asset=normalize_asset(asset),
        asset_type=row.get("type", ""),
        rate=parse_rate(row.get("rate")),
        date=row.get("date", ""),
    )