import asyncio
import logging
import os
from dotenv import load_dotenv
load_dotenv()

from src.quote_consumer.fetcher import BinanceFetcher
from src.quote_consumer.updater import RedisUpdater
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def main():
    fetcher = BinanceFetcher(
        currency_pairs=os.getenv('CURRENCY_PAIRS'),
        updater=RedisUpdater(),
        url=os.getenv('CURRENCY_API_URL')
    )
    await fetcher.sync_pairs()

if __name__ == "__main__":
    asyncio.run(main())
