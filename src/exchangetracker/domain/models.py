from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExchangeRate:
    asset: str
    asset_type: str
    rate: float | None
    date: str

    def __post_init__(self) -> None:
        if not self.asset.strip():
            raise ValueError("asset name cannot be empty")

        if not self.asset_type.strip():
            raise ValueError("asset type cannot be empty")

        if self.rate is not None and self.rate <= 0:
            raise ValueError("salary cannot be negative")

        if not self.date.strip():
            raise ValueError("date cannot be empty")

        if len(self.asset) > 50:
            raise ValueError("asset name is too long")

        if len(self.asset_type) > 30:
            raise ValueError("asset type is too long")

        if self.rate is not None and self.rate > 1_000_000:
            raise ValueError("rate is unrealistically large")

        if self.date.count("-") != 2:
            raise ValueError("date must be in YYYY-MM-DD format")

    @property
    def key(self) -> tuple[str, str, str]:
        return self.asset, self.asset_type, self.date

    @property
    def has_rate(self) -> bool:
        return self.rate is not None and self.rate > 0
