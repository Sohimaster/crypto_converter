from fastapi import APIRouter

from conversions.api.v1.conversion import conversions_router

api_v1_router = APIRouter(prefix="/api/v1", tags=["core"])

api_v1_router.include_router(conversions_router)
