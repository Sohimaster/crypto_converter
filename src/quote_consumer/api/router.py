from fastapi import APIRouter

from quote_consumer.api.v1.quotes import quote_consumer_router

api_v1_router = APIRouter(prefix="/api/v1", tags=["core"])

api_v1_router.include_router(quote_consumer_router)
