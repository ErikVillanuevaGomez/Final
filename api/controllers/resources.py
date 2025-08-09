from sqlalchemy.orm import Session
from ..models import resources as model
from ..schemas import resources as schema

def create(db: Session, request: schema.ResourceCreate):
    resource = model.Resource(**request.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

def read_all(db: Session):
    return db.query(model.Resource).all()

def read_one(db: Session, item_id: int):
    resource = db.query(model.Resource).filter(model.Resource.id == item_id).first()
    if not resource:
        raise Exception("Resource not found")
    return resource

def update(db: Session, item_id: int, request: schema.ResourceUpdate):
    resource = db.query(model.Resource).filter(model.Resource.id == item_id).first()
    if not resource:
        raise Exception("Resource not found")
    for var, value in vars(request).items():
        if value is not None:
            setattr(resource, var, value)
    db.commit()
    db.refresh(resource)
    return resource

def delete(db: Session, item_id: int):
    resource = db.query(model.Resource).filter(model.Resource.id == item_id).first()
    if not resource:
        raise Exception("Resource not found")
    db.delete(resource)
    db.commit()
    return {"ok": True}
