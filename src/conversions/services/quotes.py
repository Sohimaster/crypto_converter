from abc import ABC, abstractmethod
from decimal import Decimal

import httpx
from starlette import status

from conversions.api.exceptions import QuoteNotFound
from conversions.services.dto import Rate


class IQuotesClient(ABC):
    @abstractmethod
    async def get_exchange_rate(self, from_: str, to: str) -> Rate:
        raise NotImplementedError


class QuotesClient(IQuotesClient):
    def __init__(self, quotes_url: str):
        self._quotes_url = quotes_url

    async def get_exchange_rate(self, from_: str, to: str) -> Rate:
        async with httpx.AsyncClient(base_url=self._quotes_url) as client:
            params = {"source_currency": from_, "target_currency": to}
            response = await client.get("quote", params=params)

            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise QuoteNotFound(f'Currency pair {from_}:{to} does not exist.')

            response_body = response.json()
            return Rate(value=Decimal(response_body["rate"]), updated_at=response_body["updated_at"])
