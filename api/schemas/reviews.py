from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ReviewBase(BaseModel):
    rating: float
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    sandwich_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None

class Review(ReviewBase):
    id: int
    sandwich_id: int
    review_date: Optional[datetime] = None

    class Config:
        orm_mode = True
