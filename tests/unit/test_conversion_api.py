from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock

from starlette import status

from conversions.services.dto import Rate


def test_conversion_success(mock_quotes_client, conversion_api_client):
    mock_quotes_client.get_exchange_rate = AsyncMock(
        return_value=Rate(
            value=Decimal("1.23"),
            updated_at=datetime.now(),
        )
    )
    params = {
        "from": "USDT",
        "to": "BTC",
        "amount": 1000,
    }

    response = conversion_api_client.get(url="api/v1/conversion", params=params)

    assert response.status_code == status.HTTP_200_OK, response.json()


def test_conversion_rates_outdated_fail(mock_quotes_client, conversion_api_client):
    mock_quotes_client.get_exchange_rate = AsyncMock(
        return_value=Rate(
            value=Decimal("1.23"),
            updated_at=datetime.now() - timedelta(minutes=1),
        )
    )
    params = {
        "from": "USDT",
        "to": "BTC",
        "amount": 1000,
    }

    response = conversion_api_client.get(url="api/v1/conversion", params=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json() == {"message": "Exchange rates are older than one minute."}


def test_conversion_schema_fail(conversion_api_client):
    params = {
        "bad_param": "USDT",
        "to": "BTC",
        "amount": "str",
    }

    response = conversion_api_client.get(url="api/v1/conversion", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()
    assert response.json() == {
        "errors": [
            {
                "field": "from",
                "error": "Field required"
            },
            {
                "field": "amount",
                "error": "Input should be a valid decimal"
            },
        ]
    }
