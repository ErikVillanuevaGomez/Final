from sqlalchemy.orm import Session
from datetime import datetime
from ..models import promotions as model
from ..schemas import promotions as schema

def create(db: Session, request: schema.PromotionCreate):
    promo = model.Promotion(**request.dict())
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def read_all(db: Session):
    return db.query(model.Promotion).all()

def read_one(db: Session, item_id: int):
    promo = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
    if not promo:
        raise Exception("Promotion not found")
    return promo

def update(db: Session, item_id: int, request: schema.PromotionUpdate):
    promo = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
    if not promo:
        raise Exception("Promotion not found")
    for var, value in vars(request).items():
        if value is not None:
            setattr(promo, var, value)
    db.commit()
    db.refresh(promo)
    return promo

def delete(db: Session, item_id: int):
    promo = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
    if not promo:
        raise Exception("Promotion not found")
    db.delete(promo)
    db.commit()
    return {"ok": True}
