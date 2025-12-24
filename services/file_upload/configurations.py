from typing import Any

from pydantic import Field, BaseModel, model_validator
from pydantic_settings import BaseSettings


class _DatabaseSettings(BaseSettings):
    user: str = Field(alias="POSTGRES_USER", alias_priority=True)
    password: str = Field(alias="POSTGRES_PASSWORD", alias_priority=True)
    database: str = Field(alias="POSTGRES_DB", alias_priority=True)


class _RabbitmqSettings(BaseSettings):
    user: str = Field( alias="RABBITMQ_USER", alias_priority=True)
    password: str = Field(alias="RABBITMQ_PASS", alias_priority=True)


class _DevelopmentModeSettings(BaseSettings):
    development_mode: bool = Field(alias="DEVELOPMENT_MODE", default=False, alias_priority=True)


class _JwtSettings(BaseModel):
    public_key: str
    private_key: str

    @model_validator(mode='before')
    @classmethod
    def load_keys(cls, data: Any) -> Any:
        with open("/file_upload/crypt_keys/jwt_keys/private_key.pem", 'r') as f:
            data['private_key'] = f.read()
        with open("/file_upload/crypt_keys/jwt_keys/public_key.pem", 'r') as f:
            data['public_key'] = f.read()
        return data


class _MinioSettings(BaseSettings):
    access_key: str = Field(alias="MINIO_USER", alias_priority=True)
    access_secret: str = Field(alias="MINIO_PASSWORD", alias_priority=True)


database_settings = _DatabaseSettings()
rabbitmq_settings = _RabbitmqSettings()
development_mode_settings = _DevelopmentModeSettings()
jwt_settings = _JwtSettings()
minio_settings = _MinioSettings()
