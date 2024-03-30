import datetime
import json
import logging
import time
from abc import ABC, abstractmethod, ABCMeta
from decimal import Decimal

import redis.asyncio

from config import settings, StorageEnum
from quote_consumer.services.dto import Quote


class Singleton(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IQuoteStorage(ABC):
    @abstractmethod
    async def get_quote(self, source_currency: str, target_currency: str):
        raise NotImplementedError()

    @abstractmethod
    async def set_quote(self, source_currency: str, target_currency: str, rate: Decimal):
        raise NotImplementedError()


class RedisQuoteStorage(IQuoteStorage, metaclass=Singleton):
    def __init__(self, storage: redis.asyncio.Redis, expiration_time: int):
        self._expiration_time = expiration_time
        self._storage = storage

    async def get_quote(self, source_currency: str, target_currency: str) -> Quote:
        value = await self._storage.get(self._get_key(source_currency, target_currency))
        if not value:
            raise
        value = json.loads(value)
        return Quote(
            source_currency=source_currency,
            target_currency=target_currency,
            rate=Decimal(value["rate"]),
            updated_at=datetime.datetime.fromtimestamp(value["timestamp"]),
        )

    async def set_quote(self, source_currency: str, target_currency: str, rate: Decimal):
        value = json.dumps({"rate": str(rate), "timestamp": time.time()})
        await self._storage.setex(self._get_key(source_currency, target_currency), self._expiration_time, value)
        logging.info(f"Saved to redis: {source_currency} -> {target_currency}. Rate: {rate}")

    @staticmethod
    def _get_key(source_currency: str, target_currency: str):
        return f"currency_pair:{source_currency}_{target_currency}"


class StorageFactory:
    @classmethod
    def get_storage(cls):
        if settings.STORAGE == StorageEnum.REDIS:
            redis_client = redis.asyncio.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
            )
            return RedisQuoteStorage(redis_client, settings.REDIS_EXPIRATION_TIME)
