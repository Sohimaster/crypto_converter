from datetime import datetime, timezone
from decimal import Decimal
from unittest import mock
from unittest.mock import AsyncMock

import pytest
from starlette import testclient
from starlette.testclient import TestClient

from config import settings
from conversions.api import deps as conversions_deps
from conversions.app import app as conversion_app
from conversions.services.dto import Rate
from conversions.services.quotes import QuotesClient
from quote_consumer.api import deps as consumer_deps
from quote_consumer.app import app as consumer_app
from quote_consumer.services.storage import IQuoteStorage


@pytest.fixture(scope="session")
def conversion_api_client(mock_quotes_client) -> testclient.TestClient:
    conversion_app.dependency_overrides[conversions_deps.get_quotes_service] = lambda: mock_quotes_client
    test_client = testclient.TestClient(conversion_app)
    return test_client


@pytest.fixture(scope="session")
def mock_quotes_client():
    return mock.create_autospec(QuotesClient)


@pytest.fixture(scope="session")
def quote_consumer_api_client(mock_quotes_storage) -> testclient.TestClient:
    consumer_app.dependency_overrides[consumer_deps.get_quotes_storage] = lambda: mock_quotes_storage
    test_client = testclient.TestClient(consumer_app)
    return test_client


@pytest.fixture(scope="session")
def mock_quotes_storage():
    return mock.create_autospec(IQuoteStorage)
