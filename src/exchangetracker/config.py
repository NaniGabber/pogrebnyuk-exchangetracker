from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    data_path: str = "data/large.jsonl"
    log_level: str = "INFO"


settings = Settings()
