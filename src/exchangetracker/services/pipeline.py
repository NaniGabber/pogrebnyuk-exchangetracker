from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import islice
from typing import TypeVar
import logging

from pydantic import ValidationError

from ..domain.models import ExchangeRate
from .ports import Source
from .schemas import ExchangeRateIn

logger = logging.getLogger(__name__)

T = TypeVar("T")


def batched[T](items: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    iterator = iter(items)

    while batch := tuple(islice(iterator, size)):
        yield batch


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0

    by_asset: Counter[str] = field(default_factory=Counter)
    by_source: Counter[str] = field(default_factory=Counter)

    rate_count: int = 0
    rate_sum: float = 0.0
    rate_min: float | None = None
    rate_max: float | None = None

    @property
    def rate_avg(self) -> float | None:
        if not self.rate_count:
            return None

        return self.rate_sum / self.rate_count


class Pipeline:
    def __init__(self, sources: list[Source]) -> None:
        self._sources = sources

    def run(self) -> PipelineStats:
        stats = PipelineStats()
        logger.info("start processing %d source(s)", len(self._sources))
        seen: set[ExchangeRate] = set()

        for source in self._sources:
            for rate in self._parse(source, stats):
                if rate in seen:
                    stats.duplicates += 1
                    continue

                seen.add(rate)

                stats.kept += 1
                stats.by_source[source.name] += 1
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
        logger.info(
            "done: kept %d, invalid %d, duplicates %d",
            stats.kept,
            stats.invalid,
            stats.duplicates,
        )
        if stats.invalid:
            logger.warning("skipped %d invalid rows", stats.invalid)
        return stats

    @staticmethod
    def _parse(
        source: Source,
        stats: PipelineStats,
    ) -> Iterator[ExchangeRate]:
        for row in source.read():
            stats.read += 1

            try:
                yield ExchangeRateIn.model_validate(row).to_domain()
            except ValidationError as exc:
                stats.invalid += 1
                logger.debug("skip row: %d validation errors", exc.error_count())
