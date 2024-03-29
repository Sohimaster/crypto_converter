from config import settings
from conversions.services.quotes import QuotesClient


def get_quotes_service():
    return QuotesClient(settings.QUOTES_BASE_URL)
