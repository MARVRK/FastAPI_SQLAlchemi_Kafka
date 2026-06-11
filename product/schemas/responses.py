from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    product: str
    available_amount: int

    model_config = {"from_attributes": True}
