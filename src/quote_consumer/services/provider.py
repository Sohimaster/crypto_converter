import asyncio
import json
import ssl
from decimal import Decimal
from typing import Dict

import websockets
from websockets import WebSocketException

from config import settings, ProviderEnum
from quote_consumer.services.storage import IQuoteStorage, StorageFactory

import logging


class BaseRatesProvider:

    def __init__(self, url: str, currency_pairs: str, storage: IQuoteStorage):
        self.url = url
        self.currency_pairs = self._parse_currency_pairs(currency_pairs)
        self.storage = storage

    @staticmethod
    def _parse_currency_pairs(pairs: str) -> Dict[str, Dict[str, str]]:
        pair_dict = {}
        for pair in pairs.split(","):
            source, target = pair.split(":")
            pair = f"{source}{target}".lower()
            pair_dict[pair] = {"source": source, "target": target}
        return pair_dict

    def sync_pairs(self):
        raise NotImplementedError()


class BinanceRatesProvider(BaseRatesProvider):
    async def sync_pairs(self):
        while True:
            try:
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                async with websockets.connect(self.url, ssl=ssl_context) as websocket:
                    for pair in self.currency_pairs:
                        subscribe_message = json.dumps({"method": "SUBSCRIBE", "params": [f"{pair}@ticker"], "id": 1})
                        await websocket.send(subscribe_message)
                        await asyncio.sleep(1)
                        logging.info(f"Subscribed to {pair}@ticker")

                    while True:
                        message = await websocket.recv()
                        message_data = json.loads(message)
                        stream = message_data.get("stream", "")
                        await asyncio.sleep(1)
                        if stream:
                            pair = stream.split("@")[0]
                            pair_data = self.currency_pairs[pair]
                            source = pair_data["source"]
                            target = pair_data["target"]
                            rate = Decimal(message_data["data"]["c"])
                            await self.storage.set_quote(source_currency=source, target_currency=target, rate=rate)
                            logging.info(f"Updated {source} -> {target}. Rate: {rate}")
            except WebSocketException as e:
                logging.warning(f"WebSocket issue: {e}. Reconnecting...")
                continue
            except asyncio.exceptions.CancelledError:
                logging.info("Asyncio task cancelled. Exiting...")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}. Stopping...")
                break


class ProviderFactory:
    @classmethod
    def get_provider(cls):
        storage = StorageFactory.get_storage()
        if settings.PROVIDER == ProviderEnum.BINANCE:
            return BinanceRatesProvider(settings.BINANCE_API_URL, settings.CURRENCY_PAIRS, storage)
