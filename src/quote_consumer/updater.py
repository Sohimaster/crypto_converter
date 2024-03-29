import json
import logging
import time
from decimal import Decimal

import redis


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseStorage(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def _get_inverse_rate(rate):
        return 1 / float(rate)

    def update_pair(self, source_currency: str, target_currency: str, rate: float):
        self._save_to_storage(
            source_currency=source_currency,
            target_currency=target_currency,
            rate=Decimal(rate).quantize(Decimal('1.000000000000'))
        )
        # Save the rate for the reverse pair
        inverse_rate = self._get_inverse_rate(rate)
        self._save_to_storage(
            source_currency=target_currency,
            target_currency=source_currency,
            rate=Decimal(inverse_rate).quantize(Decimal('1.000000000000'))
        )

    def _save_to_storage(self, source_currency: str, target_currency: str, rate: float):
        raise NotImplementedError()


class RedisStorage(BaseStorage):
    def __init__(self):
        self.storage = redis.Redis(host='localhost', port=6379, db=0)

    def _save_to_storage(self, source_currency: str, target_currency: str, rate: float):
        rate_str = str(rate)
        key = f"currency_pair:{source_currency}_{target_currency}"
        value = json.dumps({
            "rate": rate_str,
            "timestamp": time.time()
        })
        self.storage.setex(key, 604800, value)
        logging.info(f"Saved to redis: {source_currency} -> {target_currency}. Rate: {rate_str}")
