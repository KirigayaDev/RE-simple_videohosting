from pydantic import Field
from pydantic_settings import BaseSettings


class _DatabaseSettings(BaseSettings):
    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    database: str = Field(..., alias="POSTGRES_DB")


class _RabbitmqSettings(BaseSettings):
    user: str = Field(..., alias="RABBITMQ_USER")
    password: str = Field(..., alias="RABBITMQ_PASS")


class _DevelopmentModeSettings(BaseSettings):
    development_mode: bool = Field(alias="DEVELOPMENT_MODE", default=False)


database_settings = _DatabaseSettings()
rabbitmq_settings = _RabbitmqSettings()
development_mode_settings = _DevelopmentModeSettings()
