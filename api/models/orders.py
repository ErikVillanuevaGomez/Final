from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from ..dependencies.database import Base
import uuid


class OrderStatus(PyEnum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(300))
    order_type = Column(String(20), default="takeout")  # or delivery
    tracking_number = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    payment_status = Column(String(20), default="unpaid")
    promo_code = Column(String(50), nullable=True)  # store promo code applied

    order_details = relationship("OrderDetail", back_populates="order")
