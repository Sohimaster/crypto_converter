from unittest import mock

from starlette import status


# @mock.patch('conversions.services.quotes.QuotesClient.get_exchange_rate', return_value=)
def test_conversion_success(mock_quotes_client, conversion_api_client):
    params = {
        'from': 'USDT',
        'to': 'BTC',
        'amount': 1000,
    }
    response = conversion_api_client.get(url='api/v1/conversion', params=params)
    assert response.status_code == status.HTTP_200_OK, response.json()


def test_conversion_rates_outdated_fail():
    pass


def test_conversion_schema_fail():
    response = conversion_api_client.get(url='api/v1/conversion')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

