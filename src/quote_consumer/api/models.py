from datetime import datetime
from decimal import Decimal

import pydantic
from pydantic import BaseModel, field_validator


class Response(BaseModel):
    pass


class QuoteResponse(Response):
    rate: Decimal
    updated_at: datetime


class Request(BaseModel):
    pass


class QuoteRequest(Request):
    source_currency: str = pydantic.Field(to_upper=True)
    target_currency: str = pydantic.Field(to_upper=True)

    @field_validator('source_currency', 'target_currency', mode='before')
    def convert_to_upper(cls, value: str):
        return value.upper()
