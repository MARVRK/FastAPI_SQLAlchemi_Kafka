from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: int
    product: str
    available_amount: int

    model_config = ConfigDict(from_attributes=True)
