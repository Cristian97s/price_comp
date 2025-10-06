from pydantic import BaseModel
from typing import Optional

class StoreBase(BaseModel):
    name: str
    url: str

class StoreCreate(StoreBase):
    pass

class StoreRead(StoreBase):
    id: int

    model_config = {
        "from_attributes": True  # Reemplaza orm_mode=True en Pydantic v2
    }