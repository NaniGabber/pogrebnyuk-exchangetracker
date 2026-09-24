from exchangetracker.domain.parsing import to_exchange_rate


def test_non_numeric_rate_becomes_none():
    row = {"date": "2026-10-10", "asset": "CHF", "type": "currency", "rate": "сорок два"}

    exchange_rate = to_exchange_rate(row)

    assert exchange_rate.rate is None
