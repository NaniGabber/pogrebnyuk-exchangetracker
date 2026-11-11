from time import perf_counter

from sqlalchemy import delete
from sqlalchemy.orm import Session

from exchangetracker.config import Settings
from exchangetracker.storage.db import make_engine
from exchangetracker.storage.models import ExchangeRateORM

settings = Settings()

engine = make_engine(settings.database_url)

ROWS = 20_000


with Session(engine) as session:
    session.execute(delete(ExchangeRateORM))
    session.commit()

    start = perf_counter()

    for i in range(ROWS):
        session.add(
            ExchangeRateORM(
                asset=f"USD{i}",
                asset_type="currency",
                date="2026-11-11",
                rate=40.0,
            )
        )

        session.commit()

    per_row = perf_counter() - start

    print(f"commit every row: {per_row:.2f}s")


with Session(engine) as session:
    session.execute(delete(ExchangeRateORM))
    session.commit()

    start = perf_counter()

    for i in range(ROWS):
        session.add(
            ExchangeRateORM(
                asset=f"EUR{i}",
                asset_type="currency",
                date="2026-11-11",
                rate=40.0,
            )
        )

    session.commit()

    single_commit = perf_counter() - start

    print(f"single commit: {single_commit:.2f}s")
    print(f"speedup: {per_row / single_commit:.1f}x")
