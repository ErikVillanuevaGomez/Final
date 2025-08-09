from sqlalchemy.orm import Session
from ..models import recipes as model
from ..schemas import recipes as schema

def create(db: Session, request: schema.RecipeCreate):
    recipe = model.Recipe(**request.dict())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def read_all(db: Session):
    return db.query(model.Recipe).all()

def read_one(db: Session, item_id: int):
    recipe = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
    if not recipe:
        raise Exception("Recipe not found")
    return recipe

def update(db: Session, item_id: int, request: schema.RecipeUpdate):
    recipe = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
    if not recipe:
        raise Exception("Recipe not found")
    for var, value in vars(request).items():
        if value is not None:
            setattr(recipe, var, value)
    db.commit()
    db.refresh(recipe)
    return recipe

def delete(db: Session, item_id: int):
    recipe = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
    if not recipe:
        raise Exception("Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"ok": True}
