from decimal import Decimal, ROUND_HALF_UP

import pydantic
from fastapi.params import Query
from pydantic import BaseModel, field_serializer


class Response(BaseModel):
    pass


class ConversionResponse(Response):
    rate: Decimal
    amount: Decimal

    @field_serializer("amount")
    def amount_serializer(self, value: Decimal):
        return str(value.quantize(Decimal(".000000"), rounding=ROUND_HALF_UP))

    @field_serializer("rate")
    def rate_serializer(self, value: Decimal):
        return str(value.quantize(Decimal(".000000000000"), rounding=ROUND_HALF_UP))


class Request(BaseModel):
    pass


class ConversionRequest(Request):
    from_: str = pydantic.Field(description="Из какой валюты переводить")
    to: str
    amount: Decimal
