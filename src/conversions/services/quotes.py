from abc import ABC, abstractmethod
from decimal import Decimal

import httpx

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
            params = {"from": from_, "to": to}
            response = await client.get("pair", params=params)
            response.raise_for_status()
            response_body = response.json()
            return Rate(value=Decimal(response_body["rate"]), updated_at=response_body["updated_at"])
