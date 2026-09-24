from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

from ..domain.models import ExchangeRate
from ..domain.parsing import to_exchange_rate
from ..sources.json_file import read_rows


def deduplicate(items: Iterable[ExchangeRate]) -> Iterator[ExchangeRate]:
    seen: set[tuple[str, str, str]] = set()

    for rate in items:
        if rate.key not in seen:
            seen.add(rate.key)
            yield rate


def count_by_asset(items: Iterable[ExchangeRate]) -> Counter[str]:
    return Counter(rate.asset for rate in items)


def load_exchange_rates(path: Path) -> list[ExchangeRate]:
    rows = read_rows(path)

    parsed = (to_exchange_rate(row) for row in rows)

    valid = (rate for rate in parsed if rate is not None)

    return list(deduplicate(valid))
