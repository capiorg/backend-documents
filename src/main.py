from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from api.v1.binding import own_router_v1
from di.dependencies import fastapi_dependency_overrides
from di.factory import ConfigFactory
from di.markers import SettingsAPIMarker
from settings.application import SettingsApplication


def create_application_v1() -> FastAPI:
    config = ConfigFactory()

    application = FastAPI(
        debug=False,
        docs_url=None,
        openapi_url="/v1/openapi.json",
        title="Minio Microservice",
        version="1.0.0",
        root_path="/v1",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    dependency_overrides = fastapi_dependency_overrides(config=config)
    application.dependency_overrides = dependency_overrides

    application.include_router(own_router_v1)

    return application


def get_parent_app() -> FastAPI:
    application_v1 = create_application_v1()
    application_v1_settings: SettingsApplication = (
        application_v1.dependency_overrides.get(SettingsAPIMarker)()
    )
    tags_metadata = [
        {
            "name": "v1",
            "description": "Версия API - v1. Нажмите справа для перехода в документацию",
            "externalDocs": {
                "description": "дополнительная документация",
                "url": f"{application_v1_settings.HOST}/v1/docs",
            },
        },
    ]
    application_own = FastAPI(
        openapi_tags=tags_metadata,
    )

    application_own.mount("/v1", create_application_v1())

    return application_own


app = get_parent_app()
