from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.post("/", response_model=schema.Recipe)
def create(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=List[schema.Recipe])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

@router.get("/{item_id}", response_model=schema.Recipe)
def read_one(item_id: int, db: Session = Depends(get_db)):
    recipe = controller.read_one(db=db, item_id=item_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{item_id}", response_model=schema.Recipe)
def update(item_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
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
