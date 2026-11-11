from collections.abc import Iterable

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..domain.models import ExchangeRate
from .mappers import _to_domain, _to_row
from .models import ExchangeRateORM


class SqlExchangeRateRepository:
    def __init__(
        self,
        session: Session,
        batch_size: int = 1000,
    ) -> None:
        self._session = session
        self._batch_size = batch_size

    def add_many(
        self,
        rates: Iterable[ExchangeRate],
    ) -> int:
        written = 0
        batch: list[dict[str, object]] = []

        for rate in rates:
            batch.append(_to_row(rate))

            if len(batch) >= self._batch_size:
                written += self._flush(batch)
                batch.clear()

        if batch:
            written += self._flush(batch)

        return written

    def count(self) -> int:
        return (
            self._session.scalar(
                select(func.count()).select_from(
                    ExchangeRateORM,
                )
            )
            or 0
        )

    def _flush(
        self,
        batch: list[dict[str, object]],
    ) -> int:
        stmt = (
            insert(ExchangeRateORM)
            .values(batch)
            .on_conflict_do_nothing(constraint="uq_exchange_rate")
            .returning(ExchangeRateORM.id)
        )

        result = self._session.execute(stmt)
        inserted = len(result.scalars().all())

        return inserted

    def by_asset(
        self,
        asset: str,
    ) -> list[ExchangeRate]:
        rows = self._session.scalars(
            select(ExchangeRateORM)
            .where(ExchangeRateORM.asset == asset)
            .order_by(ExchangeRateORM.date)
        ).all()

        return [_to_domain(row) for row in rows]

    def top_assets(
        self,
        limit: int = 10,
    ) -> list[tuple[str, int]]:
        rows = self._session.execute(
            select(
                ExchangeRateORM.asset,
                func.count().label("total"),
            )
            .group_by(ExchangeRateORM.asset)
            .order_by(func.count().desc())
            .limit(limit)
        ).all()

        return [(asset, total) for asset, total in rows]

    def average_rate(self) -> float:
        value = self._session.scalar(
            select(func.avg(ExchangeRateORM.rate)).where(
                ExchangeRateORM.rate.is_not(None),
            )
        )

        return float(value or 0.0)
