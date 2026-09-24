import json
from pathlib import Path
from collections.abc import Iterator


def read_jsonl_lazy(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def read_jsonl_eager(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]