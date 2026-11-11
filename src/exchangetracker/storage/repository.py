from collections.abc import Iterable

from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from ..domain.models import ExchangeRate
from .mappers import _to_row
from .models import ExchangeRateORM


class SqlExchangeRateRepository:
    def __init__(
        self,
        session: Session,
        batch_size: int = 1000,
    ) -> None:
        self._session = session
        self._batch_size = batch_size

    def add_many(self, rates: Iterable[ExchangeRate]) -> int:
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
        return self._session.scalar(select(func.count()).select_from(ExchangeRateORM)) or 0

    def _flush(self, batch: list[dict[str, object]]) -> int:
        stmt = (
            insert(ExchangeRateORM)
            .values(batch)
            .on_conflict_do_nothing(
                index_elements=[
                    "asset",
                    "asset_type",
                    "date",
                ]
            )
        )

        self._session.execute(stmt)
        self._session.commit()

        return len(batch)
