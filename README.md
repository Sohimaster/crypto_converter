![pytest workflow](https://github.com/Sohimaster/crypto_converter/actions/workflows/pytest.yml/badge.svg)
![Pylint workflow](https://github.com/Sohimaster/crypto_converter/actions/workflows/pylint.yml/badge.svg)
![Python version](https://img.shields.io/badge/python-3.11-blue.svg)
![fastapi](https://img.shields.io/badge/FastAPI-005571)

# Crypto Converter
Crypto Converter is a project designed to provide an API for converting amounts between cryptocurrencies using HTTP JSON API. It does not perform actual currency operations/transfers but calculates the conversion based on current quotes. The project consists of two main components running as separate processes: the Currency Conversion API and the Quote Consumer.

## Getting Started

### Requirements
- Docker
- Docker Compose

### Configuration
Both components are configurable using environment variables. Configuration details should be set in the `.env` file.

### Running the Project
1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run `docker-compose up` to start both the Currency Conversion API and the Quote Consumer services.

###
Swagger Docs
Docs are available at http://localhost:8000/docs#/

### Usage
To convert an amount from one cryptocurrency to another, use the `/api/v1/conversion` endpoint with `from`, `to`, and `amount` as HTTP GET query parameters. For example:

`GET /api/v1/conversion?from=BTC&to=USDT&amount=2`

This will return a JSON response containing the converted amount and the conversion rate used.

```
{
  "rate": "70006.050000000000",
  "amount": "140012.100000"
}
```

## Components

### Currency Conversion API
- Provides a simple conversion API accepting `from`, `to`, and `amount` as parameters.
- Returns the amount in the target currency and the conversion rate used.
- Supports precision of 6 decimal digits for amounts and 12 decimal digits for rates.
- Uses the latest available quotes from the Quote Consumer.

### Quote Consumer
- Subscribes to quotes from cryptocurrency exchanges (e.g., Binance/Coinbase) and saves them into storage.
- Updates the stored quotes in real time using websockets and removes quotes older than 7 days.

## Switching Between Exchange APIs
The Crypto Converter project supports fetching real-time cryptocurrency quotes from two major exchange APIs: Binance and Coinbase. By default, the project is configured to use Coinbase as the primary source for cryptocurrency quotes.

To switch between the Binance and Coinbase APIs, you can modify the `PROVIDER` variable in the `.env` file. Here’s how:

- To use **Binance** for fetching quotes, set `PROVIDER=binance` in your `.env` file.
- To use **Coinbase** (the default setting), ensure `PROVIDER=coinbase` is set in your `.env` file, or simply remove the setting from .env file.

After updating the `.env` file, restart the Crypto Converter services for the changes to take effect. This can be done by running `docker-compose down` followed by `docker-compose up` in the project root directory.

## Precision and Rounding

- **Decimal Calculations**: Uses Python's `Decimal` with default precision of 28 decimal places for accurate currency calculations.
- **Rounding**: At the API response stage, amounts are rounded to 6 decimal digits, and conversion rates to 12, using the `ROUND_HALF_UP` method.

## Libraries Used

This project uses several key Python libraries:

- **[FastAPI](https://fastapi.tiangolo.com/)** (`fastapi==0.110.0`): A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

- **[Uvicorn](https://www.uvicorn.org/)** (`uvicorn==0.29.0`): A lightning-fast ASGI server implementation, serving as the web server for FastAPI applications.

- **[Pydantic](https://pydantic-docs.helpmanual.io/)** (`pydantic==2.6.4`): Data validation and settings management using Python type annotations.

- **[Redis](https://redis.io/)** (`redis==5.0.3`): This project uses Redis for caching and storing real-time quotes.

- **[WebSockets](https://websockets.readthedocs.io/en/stable/)** (`websockets==12.0`): A library for building WebSocket servers and clients in Python with a focus on correctness and simplicity. Used for real-time communication with cryptocurrency exchange APIs.

The project also uses `pydantic-settings` for managing project settings through environment variables.


## Contributions
Contributions are welcome! Please feel free to submit a pull request or create an issue for any bugs or feature requests.

## License
[MIT License](LICENSE)
