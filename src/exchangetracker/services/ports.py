from collections.abc import Iterable, Iterator
from typing import Any, Protocol

from exchangetracker.domain.models import ExchangeRate


class Source(Protocol):
    """Будь-що, що віддає сирі записи для конвеєра."""

    name: str

    def read(self) -> Iterator[dict[str, Any]]: ...


class ExchangeRateRepository(Protocol):
    def add_many(self, rates: Iterable[ExchangeRate]) -> int: ...

    def count(self) -> int: ...

    def by_asset(self, asset: str) -> list[ExchangeRate]: ...

    def top_assets(self, limit: int = 10) -> list[tuple[str, int]]: ...

    def average_rate(self) -> float: ...
