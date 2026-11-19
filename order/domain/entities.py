from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from order.domain.enums import OrderStatus


@dataclass(frozen=True)
class ProductsFromOrder:

    product_id: int
    quantity: int
    price_at_time: Decimal

@dataclass(frozen=True)
class PlacedOrder:

    order_number: UUID
    status: OrderStatus
    items: tuple[ProductsFromOrder,...]

@dataclass(frozen=True)
class CartItem:
    product_id: int
    quantity: int