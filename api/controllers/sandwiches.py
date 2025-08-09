from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import sandwiches as sandwich_model

def create(db: Session, request):
    new_sandwich = sandwich_model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        category=request.category
    )
    db.add(new_sandwich)
    db.commit()
    db.refresh(new_sandwich)
    return new_sandwich

def read_all(db: Session, category: str | None = None):
    query = db.query(sandwich_model.Sandwich)
    if category:
        query = query.filter(sandwich_model.Sandwich.category.ilike(f"%{category}%"))
    return query.all()

def read_one(db: Session, item_id: int):
    sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == item_id).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

def update(db: Session, item_id: int, request):
    sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == item_id).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    for var, value in vars(request).items():
        if value is not None:
            setattr(sandwich, var, value)
    db.commit()
    db.refresh(sandwich)
    return sandwich

def delete(db: Session, item_id: int):
    sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == item_id).first()
    if not sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(sandwich)
    db.commit()
    return {"detail": "Sandwich deleted"}
