import asyncio

from fastapi import FastAPI

from config import settings
from quote_consumer.api.router import api_v1_router
from quote_consumer.services.provider import ProviderFactory

app = FastAPI(
    title=settings.CONVERSIONS_SERVICE_NAME,
    contact={"name": "Sohi", "tg": "@sohimaster"},
    description="Description",
    version="0.0.1",
)

# routers
app.include_router(api_v1_router)


@app.on_event("startup")
def on_startup():
    provider = ProviderFactory.get_provider()
    task = asyncio.create_task(provider.sync_pairs())
    pass


@app.on_event("shutdown")
def on_shutdown():
    pass
