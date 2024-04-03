from datetime import datetime
from unittest.mock import AsyncMock

from starlette import status

from quote_consumer.api.exceptions import QuoteNotFound
from quote_consumer.services.dto import Quote


def test_quote_found_success(mock_quotes_storage, quote_consumer_api_client):
    quote = Quote(
        source_currency="USDT",
        target_currency="BTC",
        rate=1.3,
        updated_at=datetime.now(),
    )
    mock_quotes_storage.get_quote = AsyncMock(return_value=quote)
    params = {
        "source_currency": "USDT",
        "target_currency": "BTC",
    }

    response = quote_consumer_api_client.get(url="api/v1/quote", params=params)

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == quote.model_dump(mode="json", exclude={"source_currency", "target_currency"})


def test_quote_not_found_fail(mock_quotes_storage, quote_consumer_api_client):
    mock_quotes_storage.get_quote = AsyncMock(side_effect=QuoteNotFound("Quote USDT:BTC is not found."))
    params = {
        "source_currency": "USDT",
        "target_currency": "BTC",
    }

    response = quote_consumer_api_client.get(url="api/v1/quote", params=params)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
    assert response.json() == {"message": "Quote USDT:BTC is not found."}


def test_quote_schema_fail(quote_consumer_api_client):
    params = {
        "target_currency": "BTC",
    }

    response = quote_consumer_api_client.get(url="api/v1/quote", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()
    assert response.json() == {"source_currency": "Field required"}
