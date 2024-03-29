import asyncio
import json
from typing import Dict

import websockets
from websockets import WebSocketException

from src.quote_consumer.updater import BaseStorage

import logging


class BaseRatesProvider:

    def __init__(self, url: str, currency_pairs: str, storage: BaseStorage):
        self.url = url
        self.currency_pairs = self._parse_currency_pairs(currency_pairs)
        self.storage = storage

    @staticmethod
    def _parse_currency_pairs(pairs: str) -> Dict[str, Dict[str, str]]:
        pair_dict = {}
        for pair in pairs.split(','):
            source, target = pair.split(':')
            _pair = f'{source}{target}'.lower()
            pair_dict[_pair] = {'source': source, 'target': target}
        return pair_dict

    def sync_pairs(self):
        raise NotImplementedError()


class BinanceRatesProvider(BaseRatesProvider):
    async def sync_pairs(self):
        while True:
            try:
                async with websockets.connect(self.url) as websocket:
                    for pair in self.currency_pairs:
                        subscribe_message = json.dumps({
                            'method': 'SUBSCRIBE',
                            'params': [f'{pair}@ticker'],
                            'id': 1
                        })
                        await websocket.send(subscribe_message)
                        logging.info(f"Subscribed to {pair}@ticker")

                    while True:
                        message = await websocket.recv()
                        message_data = json.loads(message)
                        stream = message_data.get('stream', '')
                        if stream:
                            pair = stream.split('@')[0]
                            pair_data = self.currency_pairs[pair]
                            source = pair_data['source']
                            target = pair_data['target']
                            rate = message_data['data']['c']
                            self.storage.update_pair(
                                source_currency=source,
                                target_currency=target,
                                rate=rate
                            )
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
