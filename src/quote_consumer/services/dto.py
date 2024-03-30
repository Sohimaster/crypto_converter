from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Quote(BaseModel):
    source_currency: str
    target_currency: str
    rate: Decimal
    updated_at: datetime
