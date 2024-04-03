import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from starlette import status

from conversions.api import deps, models
from conversions.api.exceptions import QuoteOutdated
from conversions.services.quotes import IQuotesClient

conversions_router = APIRouter(prefix="")


@conversions_router.get(
    "/conversion",
    response_model=models.ConversionResponse,
    status_code=status.HTTP_200_OK,
)
async def conversion(
    from_: str = Query(alias="from", description="Source currency"),
    to: str = Query(description="Target currency"),
    amount: Decimal = Query(),
    quotes_client: IQuotesClient = Depends(deps.get_quotes_service),
):
    """
    :param from_: Source currency
    :param to: Target currency
    :param amount: Amount in source currency to convert
    :param quotes_client: FastAPI DI gets quotes
    ...
    raises QuotesOutdated
    ...
    :return: Converted amount
    :rtype: models.ConversionResponse
    """
    rate = await quotes_client.get_exchange_rate(from_, to)
    if datetime.datetime.now() - rate.updated_at > datetime.timedelta(minutes=1):
        raise QuoteOutdated("Exchange rates are older than one minute.")
    amount_result = amount * rate.value
    return models.ConversionResponse(amount=amount_result, rate=rate.value)
