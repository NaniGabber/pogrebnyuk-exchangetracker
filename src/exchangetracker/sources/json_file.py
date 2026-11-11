import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
