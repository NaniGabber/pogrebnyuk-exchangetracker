from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path
from dataclasses import dataclass, field
from itertools import islice

from ..domain.models import ExchangeRate
from ..domain.parsing import to_exchange_rate
from ..sources.json_file import read_rows
from ..sources.jsonl_file import read_jsonl_lazy
from typing import TypeVar

T = TypeVar("T")


def batched(items: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    iterator = iter(items)

    while batch := tuple(islice(iterator, size)):
        yield batch


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_asset: Counter = field(default_factory=Counter)

    rate_count: int = 0
    rate_sum: float = 0.0
    rate_min: float | None = None
    rate_max: float | None = None

    @property
    def rate_avg(self) -> float | None:
        if not self.rate_count:
            return None

        return self.rate_sum / self.rate_count


def collect(items: Iterable[ExchangeRate], stats: PipelineStats) -> None:
    for rate in items:
        stats.kept += 1

        stats.by_asset[rate.asset] += 1

        value = rate.rate

        if value is None:
            continue

        stats.rate_count += 1
        stats.rate_sum += value

        if stats.rate_min is None or value < stats.rate_min:
            stats.rate_min = value

        if stats.rate_max is None or value > stats.rate_max:
            stats.rate_max = value


def deduplicate(
    items: Iterable[ExchangeRate], stats: PipelineStats
) -> Iterator[ExchangeRate]:
    seen: set[tuple[str, str, str]] = set()

    for rate in items:
        if rate.key not in seen:
            seen.add(rate.key)
            yield rate
        else:
            stats.duplicates += 1


def count_by_asset(items: Iterable[ExchangeRate]) -> Counter[str]:
    return Counter(rate.asset for rate in items)


def load_exchange_rates(path: Path, stats: PipelineStats) -> Iterator[ExchangeRate]:
    def counted_rows(rows):
        for row in rows:
            stats.read += 1
            yield row

    def valid_rates(items):
        for rate in items:
            if rate is None:
                stats.invalid += 1
                continue

            yield rate

    if path.suffix == ".jsonl":
        rows = counted_rows(read_jsonl_lazy(path))
    else:
        rows = counted_rows(read_rows(path))

    parsed = (to_exchange_rate(row) for row in rows)
    valid = valid_rates(parsed)

    yield from deduplicate(valid, stats)
