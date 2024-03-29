import datetime

from fastapi import APIRouter, Depends
from starlette import status

from conversions.api import models, deps
from conversions.api.exceptions import QuotesOutdated
from conversions.services.quotes import IQuotesClient

conversions_router = APIRouter(prefix="")


@conversions_router.get(
    "/convert",
    response_model=models.ConversionResponse,
    status_code=status.HTTP_200_OK,
)
async def convert(
    conversion_request: models.ConversionRequests,
    quotes_client: IQuotesClient = Depends(deps.get_quotes_service),
):
    """
    Ручка конвертирует одну криптовалюту в другую

    :param conversion_request: схема запроса
    :param quotes_client: FastAPI DI подсасывает quotes клиента
    ...
    :raises QuotesOutdated: курс протух
    ...
    :return: возвращает кол-во конвертированых денег и курс
    :rtype: models.ConversionResponse
    """
    rate = await quotes_client.get_exchange_rate(conversion_request.from_, conversion_request.to)
    if datetime.datetime.now() - rate.updated_at > datetime.timedelta(minutes=1):
        raise QuotesOutdated("Exchange rates are worse than one minute")
    amount_result = conversion_request.amount / rate.value
    return models.ConversionResponse(amount=amount_result, rate=rate.value)
