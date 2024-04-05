import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from starlette import status

from conversions.api import deps, models
from conversions.api.exceptions import QuoteOutdated
from conversions.api.models import ValidationErrorResponse
from conversions.services.quotes import IQuotesClient

conversions_router = APIRouter(prefix="")


@conversions_router.get(
    "/conversion",
    response_model=models.ConversionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorResponse,
            "description": "Validation errors occurred",
        }
    }
)
async def conversion(
    from_: str = Query(alias="from", description="Source currency"),
    to: str = Query(description="Target currency"),
    amount: Decimal = Query(),
    quotes_client: IQuotesClient = Depends(deps.get_quotes_service),
):
    """
    Convert a specified amount from one currency to another using the latest exchange rate.

    This endpoint allows you to specify a source currency (`from`), a target currency (`to`),
    and the amount you wish to convert.
    The conversion uses real-time exchange rates provided by the connected cryptocurrency exchange.

    **Parameters**:

    - `from`: The currency code of the source currency (e.g., "BTC").
    - `to`: The currency code of the target currency (e.g., "ETH").
    - `amount`: The amount of the source currency you want to convert.

    **Returns**: A JSON object containing:

    - `amount`: The converted amount in the target currency.
    - `rate`: The exchange rate used for the conversion.

    **Raises**:

    - `QuotesOutdated`: If the exchange rates are older than one minute, indicating they may not be accurate.

    **Example request**:

    ```http
    GET /conversion?from=BTC&to=ETH&amount=1
    ```

    **Example response**:

    ```json
    {
      "amount": "0.032",
      "rate": "32.00"
    }
    ```
    """
    rate = await quotes_client.get_exchange_rate(from_, to)
    if datetime.datetime.now() - rate.updated_at > datetime.timedelta(minutes=1):
        raise QuoteOutdated("Exchange rates are older than one minute.")
    amount_result = amount * rate.value
    return models.ConversionResponse(amount=amount_result, rate=rate.value)
