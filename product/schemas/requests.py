from pydantic import BaseModel

class ProductCreate(BaseModel):
    product: str
    available_amount: int = 0


class ProductUpdate(BaseModel):
    product: str | None = None
    available_amount: int | None = None
