from collections import Counter
from collections.abc import Iterable, Iterator

from ..domain.models import ExchangeRate


def deduplicate(items: Iterable[ExchangeRate]) -> Iterator[ExchangeRate]:
    seen: set[tuple[str, str, str]] = set()

    for rate in items:
        if rate.key not in seen:
            seen.add(rate.key)
            yield rate


def count_by_asset(items: Iterable[ExchangeRate]) -> Counter[str]:
    return Counter(rate.asset for rate in items)