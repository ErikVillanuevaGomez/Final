from sqlalchemy.orm import Session
from ..models import order_details as model
from ..schemas import order_details as schema

def create(db: Session, request: schema.OrderDetailCreate):
    order_detail = model.OrderDetail(**request.dict())
    db.add(order_detail)
    db.commit()
    db.refresh(order_detail)
    return order_detail

def read_all(db: Session):
    return db.query(model.OrderDetail).all()

def read_one(db: Session, item_id: int):
    return db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()

def update(db: Session, item_id: int, request: schema.OrderDetailUpdate):
    order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    if not order_detail:
        raise Exception("OrderDetail not found")
    for var, value in vars(request).items():
        if value is not None:
            setattr(order_detail, var, value)
    db.commit()
    db.refresh(order_detail)
    return order_detail

def delete(db: Session, item_id: int):
    order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    if not order_detail:
        raise Exception("OrderDetail not found")
    db.delete(order_detail)
    db.commit()
    return {"ok": True}
