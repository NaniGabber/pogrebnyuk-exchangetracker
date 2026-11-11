from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


def make_engine(
    database_url: str,
    echo: bool = False,
) -> Engine:
    return create_engine(database_url, echo=echo, future=True)


def make_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
