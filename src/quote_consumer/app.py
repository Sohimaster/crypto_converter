import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config import settings
from quote_consumer.api.exception_handlers import (
    base_api_exception_handler, validation_exception_handler)
from quote_consumer.api.exceptions import BaseApiException
from quote_consumer.api.router import api_v1_router
from quote_consumer.services.provider import ProviderFactory


@asynccontextmanager
async def lifespan(_: FastAPI):
    provider = ProviderFactory.get_provider()
    asyncio.create_task(provider.sync_pairs())  # noqa
    yield


app = FastAPI(
    title=settings.CONVERSIONS_SERVICE_NAME,
    description="Description",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(api_v1_router)

# exception handlers
app.exception_handler(BaseApiException)(base_api_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)
