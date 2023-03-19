from di.factory import ConfigFactory
from di.markers import BaseHTTPMarker
from di.markers import BaseSessionMarker
from di.markers import CoreServiceHTTPMarker
from di.markers import MinioFactoryMarker
from di.markers import MinioHTTPServiceMarker
from di.markers import DocumentServiceMarker
from di.markers import SessionFactoryMarker
from di.markers import SettingsAPIMarker
from di.markers import SettingsMinioMarker
from di.providers import FastAPIDependenciesProvider


def fastapi_dependency_overrides(config: ConfigFactory):
    dependencies_provider = FastAPIDependenciesProvider(config)

    return {
        SettingsAPIMarker: dependencies_provider.get_settings_app,
        SettingsMinioMarker: dependencies_provider.get_settings_minio,
        MinioFactoryMarker: dependencies_provider.get_minio_factory,
        MinioHTTPServiceMarker: dependencies_provider.get_minio_service,
        SessionFactoryMarker: dependencies_provider.get_session_factory,
        BaseSessionMarker: dependencies_provider.get_base_session,
        DocumentServiceMarker: dependencies_provider.get_document_service,
        BaseHTTPMarker: dependencies_provider.get_http_client,
        CoreServiceHTTPMarker: dependencies_provider.get_core_http_service,
    }
