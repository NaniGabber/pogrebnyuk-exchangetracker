import logging
from pathlib import Path

import pytest

from exchangetracker.sources.jsonl import JsonlSource


def test_malformed_line_is_skipped_and_logged(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = tmp_path / "broken.jsonl"

    path.write_text(
        '{"asset":"USD","type":"currency","rate":41.5,"date":"2026-10-08"}\n'
        "{not json}\n"
        '{"asset":"EUR","type":"currency","rate":48.2,"date":"2026-10-08"}\n',
        encoding="utf-8",
    )

    caplog.set_level(
        logging.DEBUG,
        logger="exchangetracker.sources.jsonl",
    )

    rows = list(JsonlSource(path).read())

    assert len(rows) == 2
    assert "skip malformed line 2" in caplog.text
