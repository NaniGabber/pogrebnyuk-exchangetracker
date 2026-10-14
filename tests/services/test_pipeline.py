from collections.abc import Iterator
from typing import Any

from exchangetracker.services.pipeline import Pipeline


class FakeSource:
    def __init__(self, rows: list[dict[str, Any]], name: str = "fake") -> None:
        self.name = name
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self._rows


ROW = {
    "asset": "UAH",
    "asset_type": "currency",
    "rate": 45.50,
    "date": "2026-02-15",
}


def test_invalid_row_is_skipped_not_raised() -> None:
    stats = Pipeline([FakeSource([ROW, {"asset": "", "asset_type": "currency"}])]).run()
    assert stats.invalid == 1 and stats.kept == 1


def test_empty_source() -> None:
    stats = Pipeline([FakeSource([])]).run()

    assert stats.read == 0
    assert stats.invalid == 0
    assert stats.duplicates == 0
    assert stats.kept == 0


def test_duplicate_rows_are_counted() -> None:
    stats = Pipeline([FakeSource([ROW, ROW])]).run()

    assert stats.read == 2
    assert stats.duplicates == 1
    assert stats.kept == 1


def test_asset_counter() -> None:
    row2 = {
        "asset": "USD",
        "asset_type": "currency",
        "rate": 41.25,
        "date": "2026-02-15",
    }

    stats = Pipeline([FakeSource([ROW, row2])]).run()

    assert stats.by_asset["UAH"] == 1
    assert stats.by_asset["USD"] == 1
