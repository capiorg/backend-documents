from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped

from db.declarative import Base


class Document(Base):
    __tablename__ = "documents"

    uuid: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    bucket_name: Mapped[str] = Column(Text, nullable=False)
    file_name: Mapped[str] = Column(Text, nullable=False)

