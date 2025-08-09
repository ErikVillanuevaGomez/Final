from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    promo_code: str
    description: Optional[str] = None
    expiration_date: datetime
    active: Optional[bool] = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = None
    description: Optional[str] = None
    expiration_date: Optional[datetime] = None
    active: Optional[bool] = None

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True
