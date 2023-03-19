from typing import Sequence
from uuid import UUID
from uuid import uuid4

from fastapi import UploadFile

from api.dto.file import MetaFileInfoDTO
from api.dto.file import SystemFileDTO
from db.repositories.base import BaseSession
from db.repositories.documents import DocumentRepository
from db.tables import Document
from services.http.core import CoreService
from services.http.minio import MinioService


class DocumentService:
    def __init__(
        self,
        session: BaseSession,
        document_repo: DocumentRepository,
        minio_http: MinioService,
        core_http: CoreService,
    ):
        self.session = session
        self.document_repo = document_repo
        self.minio_http = minio_http
        self.core_http = core_http

    async def get_by_name(self, bucket_name: str, file_name: str) -> Document:
        async with self.session.transaction():
            document = await self.document_repo.get_by_name(
                bucket_name=bucket_name,
                file_name=file_name,
            )
            return document

    async def get_url(self, uuid: UUID) -> str:
        async with self.session.transaction():
            document = await self.document_repo.get_one(uuid=uuid)
            minio_url = await self.minio_http.get_url(
                bucket_name=document.bucket_name,
                file_name=document.file_name
            )
            return minio_url

    async def get_stats(self, uuid: UUID) -> MetaFileInfoDTO:
        async with self.session.transaction():
            document = await self.document_repo.get_one(uuid=uuid)

            return await self.minio_http.get_stats(
                bucket_name=document.bucket_name,
                file_name=document.file_name,
            )

    async def get_one(self, uuid: UUID):
        async with self.session.transaction():
            document = await self.document_repo.get_one(uuid=uuid)
            minio_url = await self.minio_http.get_url(
                bucket_name=document.bucket_name,
                file_name=document.file_name
            )
            stats = self.minio_http.get_stats(
                bucket_name=document.bucket_name,
                file_name=document
            )

    async def create_many(self, files: list[UploadFile]) -> Sequence[UUID]:
        override_files = [
            SystemFileDTO(
                file_name=f"{uuid4().hex[:8]}_{element.filename}",
                file=element,
            ) for element in files
        ]

        async with self.session.transaction():
            data = [
                dict(
                    bucket_name="capi-documents",
                    file_name=element.file_name,
                )
                for element in override_files
            ]
            created_rows = await self.document_repo.create_many(data=data)

            await self.minio_http.upload_many(
                bucket_name="capi-documents",
                files=override_files
            )

            return created_rows
