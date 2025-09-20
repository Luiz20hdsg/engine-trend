from typing import Optional
from pydantic import BaseModel

class StoreBase(BaseModel):
    name: str
    logo_url: Optional[str] = None

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int

    class Config:
        from_attributes = True
