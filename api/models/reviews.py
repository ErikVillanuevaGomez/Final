from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    rating = Column(Float, nullable=False)
    comment = Column(String(300))
    review_date = Column(DateTime, default=datetime.utcnow)

    sandwich = relationship("Sandwich", back_populates="reviews")
