from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExchangeRate:
    asset: str
    asset_type: str
    rate: float | None
    date: str

    @property
    def key(self) -> tuple[str, str, str]:
        return self.asset, self.asset_type, self.date
