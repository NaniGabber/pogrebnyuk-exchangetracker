import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def row() -> dict[str, Any]:
    return {
        "asset": "Bitcoin",
        "asset_type": "Crypto",
        "rate": "68500.50",
        "date": "2026-10-22",
    }


@pytest.fixture
def rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row,
        {
            "asset": " bitcoin ",
            "asset_type": "Crypto",
            "rate": "68500.50",
            "date": "2026-10-22",
        },
        {
            "asset": "",
            "asset_type": "Forex",
            "rate": "41.25",
            "date": "2026-10-22",
        },
        {
            "asset": "EUR",
            "asset_type": "Forex",
            "rate": None,
            "date": "2026-10-22",
        },
    ]


@pytest.fixture
def jsonl_file(tmp_path: Path, rows: list[dict[str, Any]]) -> Path:
    path = tmp_path / "exchange_rates.jsonl"
    body = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    path.write_text(body + "\n", encoding="utf-8")
    return path


class FakeSource:
    name = "test"

    def __init__(self, rows):
        self._rows = rows

    def read(self):
        yield from self._rows
