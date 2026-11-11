from pathlib import Path

from exchangetracker.sources.json_file import read_rows


def test_read_rows_skips_invalid_and_empty(
    tmp_path: Path,
) -> None:
    path = tmp_path / "rates.jsonl"

    path.write_text(
        "\n" '{"asset":"USD","rate":40.5}\n' "invalid json\n" '{"asset":"EUR","rate":42.1}\n',
        encoding="utf-8",
    )

    rows = list(read_rows(path))

    assert rows == [
        {
            "asset": "USD",
            "rate": 40.5,
        },
        {
            "asset": "EUR",
            "rate": 42.1,
        },
    ]


def test_read_rows_empty_file(
    tmp_path: Path,
) -> None:
    path = tmp_path / "rates.jsonl"

    path.write_text("", encoding="utf-8")

    assert list(read_rows(path)) == []


def test_read_rows_valid_jsonl(
    tmp_path: Path,
) -> None:
    path = tmp_path / "rates.jsonl"

    path.write_text(
        '{"asset":"USD","rate":40.5}\n',
        encoding="utf-8",
    )

    rows = list(read_rows(path))

    assert len(rows) == 1
    assert rows[0]["asset"] == "USD"
    assert rows[0]["rate"] == 40.5
