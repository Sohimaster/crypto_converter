from datetime import timezone, datetime
from decimal import Decimal
from unittest import mock
from unittest.mock import AsyncMock

import pytest
from starlette import testclient
from starlette.testclient import TestClient

from config import settings
from conversions.api import deps
from conversions.services.dto import Rate
from conversions.services.quotes import QuotesClient
from quote_consumer.app import app as consumer_app
from conversions.app import app as conversion_app


@pytest.fixture(scope="session")
def conversion_api_client(mock_quotes_client) -> testclient.TestClient:
    conversion_app.dependency_overrides[deps.get_quotes_service] = lambda: mock_quotes_client
    test_client = testclient.TestClient(conversion_app)
    return test_client


@pytest.fixture(scope="session")
def quote_consumer_api_client() -> testclient.TestClient:
    test_client = testclient.TestClient(consumer_app)
    return test_client


@pytest.fixture(scope='session')
def mock_quotes_client():
    return mock.create_autospec(QuotesClient)


@pytest.fixture(scope='session')
def mock_quote_consumer_client():
    mock_client = mock.create_autospec(QuotesClient, quotes_url=settings.QUOTES_BASE_URL)
    return mock_client
