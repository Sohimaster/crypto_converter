from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    QUOTES_BASE_URL: str
    CONVERSIONS_SERVICE_NAME: str = "conversions_api"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
