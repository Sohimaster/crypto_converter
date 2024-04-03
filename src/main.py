import logging
import sys

import uvicorn

import conversions.app
import quote_consumer.app
from config import settings

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    service = sys.argv[1]

    if service == "api":
        uvicorn.run(
            conversions.app.app,
            host=settings.CONVERSIONS_API_HOST,
            port=settings.CONVERSIONS_API_PORT,
            log_level="info",
        )
    elif service == "quote-consumer":
        uvicorn.run(
            quote_consumer.app.app,
            host=settings.QUOTES_API_HOST,
            port=settings.QUOTES_API_PORT,
            log_level="info",
        )
    else:
        raise ValueError(f"Incorrect service name: {service}")
