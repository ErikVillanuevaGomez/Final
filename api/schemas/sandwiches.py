from typing import Optional
from pydantic import BaseModel

class SandwichBase(BaseModel):
    sandwich_name: str
    price: float
    category: Optional[str] = None

class SandwichCreate(SandwichBase):
    pass

class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class Sandwich(SandwichBase):
    id: int

    class Config:
        orm_mode = True
