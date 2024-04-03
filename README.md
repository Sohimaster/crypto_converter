![pytest workflow](https://github.com/sohimaster/crypto-converter/actions/workflows/pytest.yml/badge.svg)
![Pylint workflow](https://github.com/sohimaster/crypto-converter/actions/workflows/pylint.yml/badge.svg)

# Crypto Converter

## Overview
Crypto Converter is a project designed to provide an API for converting amounts between different cryptocurrencies using HTTP JSON API. It does not perform actual currency operations/transfers but calculates the conversion based on current quotes. The project consists of two main components running as separate processes: the Currency Conversion API and the Quote Consumer.

## Getting Started

### Requirements
- Docker
- Docker Compose

### Configuration
Both components are configurable using environment variables. Configuration details such as API keys (if needed) and other preferences should be set in the `.env` file.

### Running the Project
1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run `docker-compose up` to start both the Currency Conversion API and the Quote Consumer services.

###
Swagger Docs
Docs are available at http://localhost:8000/docs#/

### Usage
To convert an amount from one cryptocurrency to another, use the `/api/v1/conversion` endpoint with `from`, `to`, and `amount` as HTTP GET query parameters. For example:

`GET /convert?from=BTC&to=USDT&amount=2`

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
- Subscribes to quotes from cryptocurrency exchanges (e.g., Binance) and saves them into storage.
- Updates the stored quotes in real time using websockets and removes quotes older than 7 days.

## Precision and Rounding

- **Decimal Calculations**: Uses Python's `Decimal` with default precision of 28 decimal places for accurate currency calculations.
- **Rounding**: At the API response stage, amounts are rounded to 6 decimal digits, and conversion rates to 12, using the `ROUND_HALF_UP` method.

## Contributions
Contributions are welcome! Please feel free to submit a pull request or create an issue for any bugs or feature requests.

## License
[MIT License](LICENSE)
