from pathlib import Path
from typing import Any
from sqlalchemy import create_engine, event, Engine


def make_engine(path: Path, echo: bool = False) -> Engine:
    engine = create_engine(f"sqlite:///{path}", echo=echo, future=True)

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(connection: Any, _record: Any) -> None:
        connection.execute("PRAGMA foreign_keys=ON")

    return engine
