import enum

from pydantic_settings import SettingsConfigDict, BaseSettings


class StorageEnum(enum.Enum):
    REDIS = "redis"


class ProviderEnum(enum.Enum):
    BINANCE = "binance"


class Settings(BaseSettings):
    CONVERSIONS_API_HOST: str = "0.0.0.0"
    CONVERSIONS_API_PORT: int = 8000
    CONVERSIONS_SERVICE_NAME: str = "conversions_api"

    QUOTES_API_HOST: str = "quote-consumer"
    QUOTES_API_PORT: int = 8080
    QUOTES_BASE_URL: str = f'http://{QUOTES_API_HOST}:{QUOTES_API_PORT}/api/v1'
    BINANCE_API_URL: str
    CURRENCY_PAIRS: str
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_EXPIRATION_TIME: int = 604800  # 7 days
    STORAGE: StorageEnum = StorageEnum.REDIS
    PROVIDER: ProviderEnum = ProviderEnum.BINANCE

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
