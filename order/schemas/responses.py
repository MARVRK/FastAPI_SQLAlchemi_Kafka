from decimal import Decimal
from collections.abc import Iterator
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field

class Item (BaseModel):
    product_id: int
    quantity: int
    price_at_time: Decimal

    model_config = ConfigDict (from_attributes=True)

class OrderResponse (BaseModel):
    order_number: UUID
    status: str
    order_items: list[Item]

    model_config = ConfigDict (from_attributes=True)

    def _line_totals (self) -> Iterator[Decimal]:
        # by order calculation of each product and share on computed_field it stores
        for item in self.order_items:
            yield item.quantity * item.price_at_time

    @computed_field
    @property
    def total (self) -> Decimal:
        return sum (self._line_totals (), Decimal(0))
