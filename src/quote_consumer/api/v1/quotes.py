from fastapi import APIRouter, Depends
from starlette import status

from quote_consumer.api import models, deps
from quote_consumer.services.storage import IQuoteStorage

quote_consumer_router = APIRouter(prefix="")


@quote_consumer_router.get(
    "/quote",
    response_model=models.QuoteResponse,
    status_code=status.HTTP_200_OK,
)
async def convert(
    quote_request: models.QuoteRequest = Depends(),
    quotes_storage: IQuoteStorage = Depends(deps.get_quotes_storage),
):
    quote = await quotes_storage.get_quote(quote_request.source_currency, quote_request.target_currency)
    return models.QuoteResponse(rate=quote.rate, updated_at=quote.updated_at)

