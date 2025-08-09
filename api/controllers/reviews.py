from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import reviews as model_reviews
from ..models import sandwiches as model_sandwiches

def create(db: Session, request):
    new_review = model_reviews.Review(**request.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def read_all(db: Session):
    return db.query(model_reviews.Review).all()

def read_one(db: Session, item_id: int):
    review = db.query(model_reviews.Review).filter(model_reviews.Review.id == item_id).first()
    if not review:
        raise Exception("Review not found")
    return review

def update(db: Session, item_id: int, request):
    review = db.query(model_reviews.Review).filter(model_reviews.Review.id == item_id).first()
    if not review:
        raise Exception("Review not found")
    for var, value in vars(request).items():
        if value is not None:
            setattr(review, var, value)
    db.commit()
    db.refresh(review)
    return review

def delete(db: Session, item_id: int):
    review = db.query(model_reviews.Review).filter(model_reviews.Review.id == item_id).first()
    if not review:
        raise Exception("Review not found")
    db.delete(review)
    db.commit()
    return {"ok": True}

def get_unpopular_dishes(db: Session, rating_threshold: float = 2.5):
    subquery = db.query(
        model_reviews.Review.sandwich_id,
        func.avg(model_reviews.Review.rating).label("avg_rating"),
        func.count(model_reviews.Review.id).label("review_count")
    ).group_by(model_reviews.Review.sandwich_id).subquery()

    low_rated = db.query(model_sandwiches.Sandwich).join(
        subquery, model_sandwiches.Sandwich.id == subquery.c.sandwich_id
    ).filter(subquery.c.avg_rating < rating_threshold).all()

    return low_rated
