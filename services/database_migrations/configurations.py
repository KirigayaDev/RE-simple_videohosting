from pydantic import Field
from pydantic_settings import BaseSettings

from singleton import Singleton


class DatabaseSettings(BaseSettings, Singleton):
    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    database: str = Field(..., alias="POSTGRES_DB")
