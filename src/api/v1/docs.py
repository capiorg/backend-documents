from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

from api.v1.swagger.render import custom_swagger_ui_html

docs_router = APIRouter()


@docs_router.get("/docs", include_in_schema=False)
async def docs_handler(request: Request):
    root_path = f'{request.scope.get("root_path", "")}/openapi.json'
    return custom_swagger_ui_html(openapi_url=root_path, title="Документация v1")


@docs_router.get("/openapi.json", include_in_schema=False)
async def docs_handler_openapi(
    request: Request,
):
    if request.app.openapi_schema:
        return request.app.openapi_schema

    open_api = get_openapi(
        title="NRI Core Microservice",
        version="v1",
        routes=request.app.routes,
        servers=[{"url": "/v1"}],
    )
    request.app.openapi_schema = open_api
    return request.app.openapi_schema
