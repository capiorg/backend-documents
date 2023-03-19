from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.base import BaseCRUD
from db.tables import Document


class DocumentRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = Document
        self.base = BaseCRUD(db_session=db_session, model=self.model)

    async def get_one(self, uuid: UUID):
        stmt = select(Document).filter(Document.uuid == uuid)
        curr = await self.db_session.execute(statement=stmt)
        return curr.scalar_one()

    async def get_by_name(self, bucket_name: str, file_name: str) -> Document:
        stmt = (
            select(Document)
            .filter(
                Document.bucket_name == bucket_name,
                Document.file_name == file_name,
            )
        )
        curr = await self.db_session.execute(statement=stmt)
        return curr.scalar_one()

    async def create_many(self, data: list[dict[str, str]]) -> Sequence[UUID]:
        model = insert(self.model).values(data).on_conflict_do_nothing().returning(self.model.uuid)
        curr = await self.db_session.execute(model)
        return curr.scalars().all()
