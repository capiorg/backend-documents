from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

from db.repositories.base import BaseSession
from db.repositories.documents import DocumentRepository
from di.factory import ConfigFactory
from di.factory import MinioFactory
from di.factory import SessionFactory
from di.markers import BaseHTTPMarker
from di.markers import BaseSessionMarker
from di.markers import CoreServiceHTTPMarker
from di.markers import MinioFactoryMarker
from di.markers import MinioHTTPServiceMarker
from di.markers import SessionFactoryMarker
from services.http.base import HTTPClient
from services.http.core import CoreService
from services.http.minio import MinioService
from services.minio import DocumentService
from settings.application import SettingsApplication
from settings.minio import SettingsMinio


class FastAPIDependenciesProvider:
    def __init__(self, config: ConfigFactory):
        self.config = config
        self.engine = create_async_engine(
            config.postgres.dsn(mode="async"),
            future=True,
            echo=False,
            connect_args={"timeout": 30},
            pool_size=100,
        )

    def get_settings_minio(self) -> SettingsMinio:
        return self.config.minio

    def get_settings_app(self) -> SettingsApplication:
        return self.config.app

    def get_session_factory(self) -> SessionFactory:
        return SessionFactory(engine=self.engine)

    def get_minio_factory(self) -> MinioFactory:
        return MinioFactory(
            settings=self.config.minio
        )

    @staticmethod
    def get_http_client():
        return HTTPClient()

    # @staticmethod
    def get_core_http_service(
        self,
        http_client: HTTPClient = Depends(BaseHTTPMarker),
    ):
        return CoreService(
            base_url=self.config.app.CORE_URL,
            client=http_client,
        )

    @staticmethod
    def get_minio_service(
        minio_factory: MinioFactory = Depends(MinioFactoryMarker),
    ) -> MinioService:
        return MinioService(client=minio_factory.session)

    @staticmethod
    def get_base_session(
        session: SessionFactory = Depends(SessionFactoryMarker),
    ):
        return BaseSession(db_session=session.session_factory)

    @staticmethod
    def get_document_service(
        session: BaseSession = Depends(BaseSessionMarker),
        minio_http: MinioService = Depends(MinioHTTPServiceMarker),
        core_http: CoreService = Depends(CoreServiceHTTPMarker),
    ):
        return DocumentService(
            session=session,
            document_repo=DocumentRepository(db_session=session.session),
            minio_http=minio_http,
            core_http=core_http,
        )
