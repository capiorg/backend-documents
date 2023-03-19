from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from settings.application import SettingsApplication
from settings.minio import SettingsMinio
from settings.postgres import SettingsPostgres


class ConfigFactory:
    def __init__(self):
        self.minio = SettingsMinio()
        self.app = SettingsApplication()
        self.postgres = SettingsPostgres()


class SessionFactory:
    def __init__(self, engine: AsyncEngine):
        self.session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )


class MinioFactory:
    def __init__(self, settings: SettingsMinio):
        self.session = Minio(
            settings.HOST,
            access_key=settings.ACCESS_KEY,
            secret_key=settings.SECRET_KEY,
            secure=True
        )
