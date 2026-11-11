import os
from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from exchangetracker.domain.models import ExchangeRate
from exchangetracker.storage.db import (
    make_engine,
    make_session_factory,
)
from exchangetracker.storage.models import Base
from exchangetracker.storage.repository import (
    SqlExchangeRateRepository,
)

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/exchangetracker"
)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = make_engine(TEST_DATABASE_URL)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    factory = make_session_factory(engine)

    db = factory()

    yield db

    db.close()
    engine.dispose()


def make_rate(
    asset: str = "USD",
    asset_type: str = "currency",
    day: int = 1,
    rate: float | None = 40.0,
) -> ExchangeRate:
    return ExchangeRate(
        asset=asset,
        asset_type=asset_type,
        date=f"2026-10-{day:02d}",
        rate=rate,
    )


def test_empty_repository(session: Session) -> None:
    repo = SqlExchangeRateRepository(session)

    assert repo.count() == 0


def test_add_rate(session: Session) -> None:
    repo = SqlExchangeRateRepository(session)

    written = repo.add_many([make_rate()])

    assert written == 1
    assert repo.count() == 1


def test_add_many_rates(session: Session) -> None:
    repo = SqlExchangeRateRepository(session)

    written = repo.add_many(
        [
            make_rate("USD"),
            make_rate("EUR"),
            make_rate("GBP"),
        ]
    )

    assert written == 3
    assert repo.count() == 3


def test_duplicate_insert_returns_zero(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    rate = make_rate()

    assert repo.add_many([rate]) == 1
    assert repo.add_many([rate]) == 0

    assert repo.count() == 1


def test_duplicate_inside_batch(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    rate = make_rate()

    written = repo.add_many(
        [
            rate,
            rate,
            rate,
        ]
    )

    assert written == 1
    assert repo.count() == 1


def test_same_date_different_assets(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    written = repo.add_many(
        [
            make_rate("USD"),
            make_rate("EUR"),
            make_rate("GBP"),
        ]
    )

    assert written == 3
    assert repo.count() == 3


def test_average_rate(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    repo.add_many(
        [
            make_rate(day=1, rate=10.0),
            make_rate(day=2, rate=20.0),
            make_rate(day=3, rate=30.0),
        ]
    )

    assert repo.average_rate() == 20.0


def test_average_rate_ignores_null(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    repo.add_many(
        [
            make_rate(day=1, rate=10.0),
            make_rate(day=2, rate=20.0),
            make_rate(day=3, rate=None),
        ]
    )

    assert repo.average_rate() == 15.0


def test_top_assets(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    repo.add_many(
        [
            make_rate("USD", day=1),
            make_rate("USD", day=2),
            make_rate("USD", day=3),
            make_rate("EUR", day=1),
            make_rate("EUR", day=2),
            make_rate("GBP", day=1),
        ]
    )

    top = repo.top_assets(3)

    assert top == [
        ("USD", 3),
        ("EUR", 2),
        ("GBP", 1),
    ]


def test_failed_transaction_rolls_back(
    session: Session,
) -> None:
    repo = SqlExchangeRateRepository(session)

    try:
        repo.add_many(
            [
                make_rate("USD"),
                make_rate("EUR"),
            ]
        )

        raise RuntimeError("boom")

    except RuntimeError:
        session.rollback()

    assert repo.count() == 0
