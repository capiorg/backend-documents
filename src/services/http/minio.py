import magic
import datetime

from fastapi import UploadFile
from miniopy_async import Minio
from api.dto.file import MetaFileInfoDTO
from api.dto.file import SizeModelDTO
from api.dto.file import SystemFileDTO
from api.utils.size import convert_size


class MinioService:
    def __init__(
        self,
        client: Minio,
    ):
        self.client = client

    async def get_url(
        self,
        bucket_name: str,
        file_name: str,
    ) -> str:
        url = await self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=file_name,
            expires=datetime.timedelta(days=2)
        )
        return url

    async def get_stats(
        self,
        bucket_name: str,
        file_name: str,
    ) -> MetaFileInfoDTO:
        stats = await self.client.stat_object(
            bucket_name=bucket_name,
            object_name=file_name,
        )
        return MetaFileInfoDTO(
            file_name=stats.object_name,
            content_type=stats.content_type,
            last_modified=stats.last_modified,
            size=SizeModelDTO(
                size=stats.size,
                human=convert_size(stats.size)
            )
        )

    async def upload(
        self,
        bucket_name: str,
        file_name: str,
        file: UploadFile,
    ) -> None:
        split_size = file.size if file.size < 2048 else 2048
        read_file = await file.read(size=split_size)
        correct_mime_type = magic.from_buffer(read_file, mime=True)
        await file.seek(0)

        await self.client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            content_type=correct_mime_type,
            data=file.file,
            length=file.size,
        )

    async def upload_many(
        self,
        bucket_name: str,
        files: list[SystemFileDTO],
    ) -> None:
        for file in files:
            await self.upload(
                bucket_name=bucket_name,
                file_name=file.file_name,
                file=file.file,
            )
