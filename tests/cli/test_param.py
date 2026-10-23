from exchangetracker.cli import main
import pytest
from pathlib import Path


def test_flag_beats_environment(jsonl_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    levels: list[str] = []
    monkeypatch.setattr("exchangetracker.cli.setup", levels.append)
    monkeypatch.setenv("LOG_LEVEL", "ERROR")
    monkeypatch.setattr("sys.argv", ["exchangetracker", str(jsonl_file), "--log-level", "DEBUG"])
    main()
    assert levels == ["DEBUG"]
