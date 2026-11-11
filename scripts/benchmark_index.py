from time import perf_counter

from sqlalchemy import text
from sqlalchemy.orm import Session

from exchangetracker.config import Settings
from exchangetracker.storage.db import make_engine

settings = Settings()

engine = make_engine(settings.database_url)


def explain(session: Session, sql: str) -> None:
    rows = session.execute(text(f"EXPLAIN ANALYZE {sql}")).all()

    print("-" * 80)

    for row in rows:
        print(row[0])

    print("-" * 80)


def benchmark(
    session: Session,
    sql: str,
    repeats: int = 100,
) -> float:
    start = perf_counter()

    for _ in range(repeats):
        session.execute(text(sql)).all()

    return perf_counter() - start


with Session(engine) as session:
    print("\n=== LOW CARDINALITY COLUMN (asset) ===")

    session.execute(text("DROP INDEX IF EXISTS idx_asset"))
    session.commit()

    sql = """
    SELECT *
    FROM exchange_rates
    WHERE asset = 'USD'
    """

    print("\nWITHOUT INDEX")

    explain(session, sql)

    elapsed = benchmark(session, sql)

    print(f"time: {elapsed:.6f}s")

    session.execute(
        text("""
            CREATE INDEX idx_asset
            ON exchange_rates(asset)
            """)
    )
    session.commit()

    print("\nWITH INDEX")

    explain(session, sql)

    elapsed = benchmark(session, sql)

    print(f"time: {elapsed:.6f}s")

    print("\n=== HIGH CARDINALITY COLUMN (date) ===")

    session.execute(text("DROP INDEX IF EXISTS idx_date"))
    session.commit()

    sql = """
    SELECT *
    FROM exchange_rates
    WHERE date = '2026-07-15'
    """

    print("\nWITHOUT INDEX")

    explain(session, sql)

    elapsed = benchmark(session, sql)

    print(f"time: {elapsed:.6f}s")

    session.execute(
        text("""
            CREATE INDEX idx_date
            ON exchange_rates(date)
            """)
    )
    session.commit()

    print("\nWITH INDEX")

    explain(session, sql)

    elapsed = benchmark(session, sql)

    print(f"time: {elapsed:.6f}s")
