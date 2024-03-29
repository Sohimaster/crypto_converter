import json
import logging
import time
import redis


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseUpdater(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def _get_inverse_rate(rate):
        return 1 / float(rate)

    def update_pair(self, source_currency: str, target_currency: str, rate: float):
        self._save_to_storage(
            source_currency=source_currency,
            target_currency=target_currency,
            rate=rate
        )
        # Save the rate for the reverse pair
        inverse_rate = self._get_inverse_rate(rate)
        self._save_to_storage(
            source_currency=target_currency,
            target_currency=source_currency,
            rate=inverse_rate
        )

    def _save_to_storage(self, source_currency: str, target_currency: str, rate: float):
        raise NotImplementedError()


class RedisUpdater(BaseUpdater):
    def __init__(self):
        self.storage = redis.Redis(host='localhost', port=6379, db=0)

    def _save_to_storage(self, source_currency: str, target_currency: str, rate: float):
        # Construct the key for the currency pair
        key = f"currency_pair:{source_currency}_{target_currency}"
        # Create a value containing the rate and the current timestamp
        value = json.dumps({
            "rate": rate,
            "timestamp": time.time()  # Current time in seconds since the Epoch
        })
        # Save the JSON string to Redis with a 7-day expiration
        self.storage.setex(key, 604800, value)
        logging.info(f"Saved to redis: {source_currency} -> {target_currency}. Rate: {rate}")
