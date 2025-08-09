from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .order_details import OrderDetail
from .promotions import Promotion

class OrderDetailCreate(BaseModel):
    sandwich_id: int
    amount: int

class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    order_type: Optional[str] = Field(default="takeout", description="Order type: takeout or delivery")
    promo_code: Optional[str] = None

class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    order_type: Optional[str] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    promo_code: Optional[str] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    order_details: List[OrderDetail] = []

    class Config:
        orm_mode = True
