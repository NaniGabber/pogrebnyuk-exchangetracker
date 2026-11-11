from pathlib import Path
from typing import Any
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker


def make_engine(path: Path, echo: bool = False) -> Engine:
    engine = create_engine(f"sqlite:///{path}", echo=echo, future=True)

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(connection: Any, _record: Any) -> None:
        connection.execute("PRAGMA foreign_keys=ON")

    return engine


def make_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
