from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Rate(BaseModel):
    value: Decimal
    updated_at: datetime
