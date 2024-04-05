from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, field_validator


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

    @field_validator("source_currency", "target_currency", mode="before")
    def convert_to_upper(cls, value: str):  # pylint: disable = E0213
        return value.upper()


class ValidationErrorItem(Response):
    field: str
    error: str


class ValidationErrorResponse(Response):
    errors: List[ValidationErrorItem]
