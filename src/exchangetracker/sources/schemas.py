from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.models import ExchangeRate


class ExchangeRateIn(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    asset: str = Field(min_length=1, max_length=50)
    asset_type: str = Field(min_length=1, alias="type")
    rate: float | None = Field(default=None, gt=0)
    date: str = Field(min_length=1)

    @field_validator("rate", mode="before")
    @classmethod
    def unknown_rate(cls, value: object) -> object:
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return None
        return value

    @field_validator("asset", "asset_type")
    @classmethod
    def strip_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("asset")
    @classmethod
    def uppercase_asset(cls, value: str) -> str:
        return value.upper()

    def to_domain(self) -> ExchangeRate:
        return ExchangeRate(
            asset=self.asset,
            asset_type=self.asset_type,
            rate=self.rate,
            date=self.date,
        )
