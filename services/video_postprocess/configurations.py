from typing import Any

from pydantic import Field, BaseModel, model_validator
from pydantic_settings import BaseSettings


class _RabbitmqSettings(BaseSettings):
    user: str = Field(alias="RABBITMQ_USER", alias_priority=True)
    password: str = Field(alias="RABBITMQ_PASS", alias_priority=True)


class _DevelopmentModeSettings(BaseSettings):
    development_mode: bool = Field(alias="DEVELOPMENT_MODE", default=False, alias_priority=True)


class _MinioSettings(BaseSettings):
    access_key: str = Field(alias="MINIO_USER", alias_priority=True)
    access_secret: str = Field(alias="MINIO_PASSWORD", alias_priority=True)


rabbitmq_settings = _RabbitmqSettings()
development_mode_settings = _DevelopmentModeSettings()
minio_settings = _MinioSettings()
