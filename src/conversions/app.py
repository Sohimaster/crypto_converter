from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config import settings
from conversions.api.exception_handlers import (
    base_api_exception_handler,
    validation_exception_handler,
)
from conversions.api.exceptions import BaseApiException
from conversions.api.router import api_v1_router

app = FastAPI(
    title=settings.CONVERSIONS_SERVICE_NAME,
    contact={"name": "Sohi", "tg": "@sohimaster"},
    description="Description",
    version="0.0.1",
)

# routers
app.include_router(api_v1_router)

# exception handlers
app.exception_handler(BaseApiException)(base_api_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)
