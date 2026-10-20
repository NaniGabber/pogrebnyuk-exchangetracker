import json
import logging

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from ..errors import SourceError

logger = logging.getLogger(__name__)


class JsonlSource:
    name = "jsonl"

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self) -> Iterator[dict[str, Any]]:
        try:
            handle = self._path.open(encoding="utf-8")
        except IOError as exc:
            raise SourceError(f"cannot open {self._path}") from exc

        with handle as f:
            for number, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    logger.debug("skip malformed line %d in %s", number, self._path)


def read_jsonl_lazy(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def read_jsonl_eager(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]
