from sqlalchemy import Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ExchangeRateORM(Base):
    __tablename__ = "exchange_rates"

    asset: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    asset_type: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
    )

    date: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
