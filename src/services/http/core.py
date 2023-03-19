from uuid import UUID

from services.http.base import HTTPClient


class CoreService:
    def __init__(
        self,
        client: HTTPClient,
        base_url: str,
    ):
        self.client = client
        self.base_url = base_url

    async def update_document(
        self,
        document_id: UUID,
        file_name: str,
        size_bytes: int,
        mime_type: str,
    ):
        await self.client.request(
            "PATCH",
            f"{self.base_url}/api/v1/documents/{document_id}",
            json={
                "file_name": file_name,
                "size_bytes": size_bytes,
                "mime_type": mime_type,
            }
        )
