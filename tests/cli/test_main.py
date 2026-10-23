from pathlib import Path

import pytest

from exchangetracker.cli import main


def test_missing_file_exits_with_code_1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing = tmp_path / "missing.jsonl"

    monkeypatch.setattr(
        "sys.argv",
        ["exchangetracker", str(missing)],
    )

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
