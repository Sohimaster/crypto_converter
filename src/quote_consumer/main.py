import asyncio
import logging
import argparse
import os

from dotenv import load_dotenv

from src.quote_consumer.fetcher import BinanceRatesProvider
from src.quote_consumer.updater import RedisStorage

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description='Currency Pair Fetcher and Updater')
    parser.add_argument('--provider', type=str, required=True, help='Data provider (e.g., "binance")')
    parser.add_argument('--storage', type=str, required=True, help='Storage option (e.g., "redis")')
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.storage == 'redis':
        storage = RedisStorage()
    else:
        raise ValueError(f"Unsupported storage: {args.storage}")

    if args.provider == 'binance':
        fetcher = BinanceRatesProvider(
            storage=storage,
            currency_pairs=os.getenv('CURRENCY_PAIRS'),
            url=os.getenv('BINANCE_API_URL'),
        )
    else:
        raise ValueError(f"Unsupported provider: {args.provider}")

    await fetcher.sync_pairs()

if __name__ == '__main__':
    asyncio.run(main())