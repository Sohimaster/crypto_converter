from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    QUOTES_BASE_URL: str
    CONVERSIONS_SERVICE_NAME: str = "conversions_api"

    BINANCE_API_URL: str
    CURRENCY_PAIRS: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
