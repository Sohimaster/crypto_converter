import asyncio
import logging
import ssl
import websockets
from websockets.exceptions import WebSocketException


class WebSocketConnectionManager:
    def __init__(self, url: str):
        self.url = url
        self.websocket = None

    async def __aenter__(self):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self.websocket = await websockets.connect(self.url, ssl=ssl_context)
            return self.websocket
        except WebSocketException as e:
            logging.warning(f"WebSocket issue during connection: {e}.")
            raise e

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.websocket:
            await self.websocket.close()
        if exc_type:
            if exc_type == asyncio.exceptions.CancelledError:
                logging.info("Asyncio task cancelled.")
            elif exc_type == WebSocketException:
                logging.warning(f"WebSocket issue: {exc_val}.")
            else:
                logging.error(f"An unexpected error occurred: {exc_val}. Stopping...")
                raise exc_val
