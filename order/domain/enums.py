from enum import Enum

class OrderStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

def get_statuses(order_status_attributes: type[Enum]):
    return [status.value for status in order_status_attributes]


