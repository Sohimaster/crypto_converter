import datetime

from fastapi import APIRouter
from starlette import status

from quote_consumer.api import models
from quote_consumer.api.exceptions import QuotesOutdated

quote_consumer_router = APIRouter(prefix="")


@quote_consumer_router.get(
    "/quote",
    response_model=models.QuoteResponse,
    status_code=status.HTTP_200_OK,
)
async def convert(
    conversion_request: models.QuoteRequest,
):
    rate = await quotes_client.get_exchange_rate(conversion_request.from_, conversion_request.to)
    if datetime.datetime.now() - rate.updated_at > datetime.timedelta(minutes=1):
        raise QuotesOutdated("Exchange rates are worse than one minute")
    amount_result = conversion_request.amount / rate.value
    return models.ConversionResponse(amount=amount_result, rate=rate.value)
