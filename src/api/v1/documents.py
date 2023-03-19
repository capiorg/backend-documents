from urllib import parse
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.responses import RedirectResponse

from api.dto.file import MetaFileInfoDTO
from api.dto.file import ResponseCreateFileDTO
from api.dto.webhook import WebhookRequestDTO
from di.markers import DocumentServiceMarker
from di.markers import MinioHTTPServiceMarker
from services.http.minio import MinioService
from services.minio import DocumentService

document_router = APIRouter()


# @document_router.get("/documents/{uuid}")
# async def get_file(
#     uuid: UUID,
#     service: DocumentService = Depends(DocumentServiceMarker),
# ):
#     document = await service.get_one(uuid=uuid)
#     return RedirectResponse(url=document.url)


@document_router.get("/documents/{uuid}/file", response_class=RedirectResponse)
async def get_file(
    uuid: UUID,
    service: DocumentService = Depends(DocumentServiceMarker),
):
    document_url = await service.get_url(uuid=uuid)
    return RedirectResponse(url=document_url)


@document_router.get("/documents/{uuid}/stats", response_model=MetaFileInfoDTO)
async def get_file(
    uuid: UUID,
    service: DocumentService = Depends(DocumentServiceMarker),
):
    return await service.get_stats(uuid=uuid)


@document_router.get("/documents/{uuid}", response_model=MetaFileInfoDTO)
async def get_file(
    uuid: UUID,
    service: DocumentService = Depends(DocumentServiceMarker),
):
    return await service.get_stats(uuid=uuid)


@document_router.post("/documents", response_model=ResponseCreateFileDTO)
async def upload_file(
    file: list[UploadFile],
    service: DocumentService = Depends(DocumentServiceMarker),
):
    uuids = await service.create_many(
        files=file,
    )
    return {"files": uuids}
