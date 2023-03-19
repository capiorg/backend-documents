from pydantic import BaseSettings
from pydantic import Field


class SettingsApplication(BaseSettings):
    HOST: str = Field(...)
    CORE_URL: str = Field(...)

    class Config:
        env_prefix = 'APPLICATION_'

        env_file = "../.env"
        env_file_encoding = "utf-8"
