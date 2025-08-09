from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    expiration_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
