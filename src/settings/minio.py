from pydantic import BaseSettings
from pydantic import Field


class SettingsMinio(BaseSettings):
    HOST: str = Field(...)
    ACCESS_KEY: str = Field(...)
    SECRET_KEY: str = Field(...)

    class Config:
        env_prefix = 'MINIO_'

        env_file = "../.env"
        env_file_encoding = "utf-8"
