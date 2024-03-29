from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Response(BaseModel):
    pass


class QuoteResponse(Response):
    rate: Decimal
    updated_at: datetime


class Request(BaseModel):
    pass


class QuoteRequest(Request):
    source_currency: str
    target_currency: str
