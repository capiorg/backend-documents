from fastapi import APIRouter

from api.v1.docs import docs_router
from api.v1.documents import document_router

own_router_v1 = APIRouter()
own_router_v1.include_router(document_router, tags=["Documents"])
own_router_v1.include_router(docs_router, tags=["Docs"])
