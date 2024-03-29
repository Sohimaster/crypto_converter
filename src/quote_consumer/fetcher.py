import json
from typing import Dict

import websockets

from src.quote_consumer.updater import BaseUpdater

import logging


class BaseFetcher:

    def __init__(self, url: str, currency_pairs: str, updater: BaseUpdater):
        self.url = url
        self.currency_pairs = self._parse_currency_pairs(currency_pairs)
        self.updater = updater

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


class BinanceFetcher(BaseFetcher):
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
                            self.updater.update_pair(
                                source_currency=source,
                                target_currency=target,
                                rate=rate
                            )
                            logging.info(f"Updated: {source} -> {target}. Rate: {rate}")
            except websockets.exceptions.ConnectionClosed:
                logging.warning("WebSocket connection closed. Reconnecting...")
                continue
            except Exception as e:
                logging.error(f"An error occurred: {e}. Restarting sync_pairs...")
            except SystemExit:
                logging.info("System exit requested. Terminating sync_pairs.")
                break
