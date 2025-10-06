from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    url: str
    store_id: int

# Para crear un producto (POST)
class ProductCreate(ProductBase):
    pass

# Para leer un producto (GET)
class ProductRead(ProductBase):
    id: int

    model_config = {
        "from_attributes": True  # Reemplaza orm_mode=True en Pydantic v2
    }
