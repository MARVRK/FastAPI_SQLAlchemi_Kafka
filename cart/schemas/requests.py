from typing import Annotated

from pydantic import BaseModel, PositiveInt,Field, field_validator
class CartProduct(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt

class CartCreateUpdate(BaseModel):
    items: Annotated[list[CartProduct],Field(min_length=1)]
    @field_validator('items',mode='after')
    @classmethod
    def check_duplicates(cls, items: list[CartProduct]) -> list[CartProduct] :
        products_by_id = [item.product_id for item in items]
        if len(set(products_by_id)) != len(products_by_id):
            raise ValueError("Items contain duplicates!")
        return items
