from typing import Literal

from pydantic import BaseSettings
from pydantic import Field
from pydantic import PostgresDsn


class SettingsPostgres(BaseSettings):
    HOST: str = Field(...)
    PORT: str = Field(...)
    USER: str = Field(...)
    PASSWORD: str = Field(...)
    DATABASE: str = Field(...)

    def dsn(self, mode: Literal["sync", "async"]):
        scheme = "postgresql+asyncpg" if mode == "async" else "postgresql"

        return PostgresDsn.build(
            scheme=scheme,
            user=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            path=f"/{self.DATABASE}",
            port=self.PORT,
        )

    class Config:
        env_prefix = 'POSTGRES_'

        env_file = "../.env"
        env_file_encoding = "utf-8"
