from pydantic import BaseModel,ConfigDict

class Item(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict (from_attributes=True)

class CartResponse(BaseModel):
    id: int | None
    items: list[Item]