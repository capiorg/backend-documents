import datetime
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel

from api.dto.base import BaseModelORM


class SizeModelDTO(BaseModelORM):
    size: int
    human: str


class MetaFileInfoDTO(BaseModelORM):
    file_name: str
    content_type: str
    last_modified: datetime.datetime
    size: SizeModelDTO


class FileInfoDTO(BaseModelORM):
    url: str
    meta: MetaFileInfoDTO


class ResponseCreateFileDTO(BaseModelORM):
    files: list[UUID]


class SystemFileDTO:
    def __init__(
        self,
        file_name: str,
        file: UploadFile,
    ):
        self.file_name = file_name
        self.file = file
