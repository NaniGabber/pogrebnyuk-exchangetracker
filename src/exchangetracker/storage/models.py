from sqlalchemy import Float, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ExchangeRateORM(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    asset: Mapped[str] = mapped_column(
        String(50),
        primary_key=False,
    )

    asset_type: Mapped[str] = mapped_column(
        String(30),
        primary_key=False,
    )

    date: Mapped[str] = mapped_column(
        String(10),
        primary_key=False,
    )

    rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "asset",
            "asset_type",
            "date",
            name="uq_exchange_rate",
        ),
    )
