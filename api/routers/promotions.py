from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..controllers import promotions as controller
from ..schemas import promotions as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)

@router.post("/", response_model=schema.Promotion)
def create(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=List[schema.Promotion])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.get("/{item_id}", response_model=schema.Promotion)
def read_one(item_id: int, db: Session = Depends(get_db)):
    promo = controller.read_one(db=db, item_id=item_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo

@router.put("/{item_id}", response_model=schema.Promotion)
def update(item_id: int, request: schema.PromotionUpdate, db: Session = Depends(get_db)):
    try:
        return controller.update(db=db, item_id=item_id, request=request)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    try:
        return controller.delete(db=db, item_id=item_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
