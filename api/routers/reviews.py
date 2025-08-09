from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..schemas import sandwiches as sandwich_schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.get("/", response_model=List[schema.Review])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/{item_id}", response_model=schema.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    try:
        return controller.read_one(db=db, item_id=item_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{item_id}", response_model=schema.Review)
def update(item_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
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

@router.get("/unpopular", response_model=List[sandwich_schema.Sandwich])
def get_unpopular_dishes(db: Session = Depends(get_db), rating_threshold: float = Query(2.5)):
    return controller.get_unpopular_dishes(db=db, rating_threshold=rating_threshold)
