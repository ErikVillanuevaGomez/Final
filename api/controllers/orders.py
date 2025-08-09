from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..models import orders as order_model, order_details as order_detail_model, resources as resource_model, promotions as promotion_model, recipes as recipe_model, sandwiches as sandwich_model
from sqlalchemy import func

def check_ingredients_availability(db: Session, order_details):
    for od in order_details:
        sandwich_recipes = db.query(recipe_model.Recipe).filter(recipe_model.Recipe.sandwich_id == od.sandwich_id).all()
        for recipe in sandwich_recipes:
            resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == recipe.resource_id).first()
            if not resource or resource.amount < (recipe.amount * od.amount):
                raise HTTPException(status_code=400, detail=f"Not enough {resource.item if resource else 'resource'} for sandwich ID {od.sandwich_id}")

def apply_promo_code(db: Session, promo_code: str, total_price: float):
    if not promo_code:
        return total_price, None
    promo = db.query(promotion_model.Promotion).filter(
        promotion_model.Promotion.promo_code == promo_code,
        promotion_model.Promotion.active == True,
        promotion_model.Promotion.expiration_date >= datetime.utcnow()
    ).first()
    if not promo:
        raise HTTPException(status_code=400, detail="Invalid or expired promo code")
    discount = total_price * 0.10
    return total_price - discount, promo.promo_code

def create(db: Session, request):
    check_ingredients_availability(db, request.order_details)

    total_price = 0.0
    for od in request.order_details:
        sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == od.sandwich_id).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail=f"Sandwich with id {od.sandwich_id} not found")
        total_price += float(sandwich.price) * od.amount

    discounted_price, applied_code = apply_promo_code(db, getattr(request, "promo_code", None), total_price)

    new_order = order_model.Order(
        customer_name=request.customer_name,
        description=request.description,
        order_type=getattr(request, "order_type", "takeout"),
        status="pending",
        payment_status="unpaid",
        promo_code=applied_code
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for od in request.order_details:
        sandwich_recipes = db.query(recipe_model.Recipe).filter(recipe_model.Recipe.sandwich_id == od.sandwich_id).all()
        for recipe in sandwich_recipes:
            resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == recipe.resource_id).first()
            resource.amount -= recipe.amount * od.amount
            db.add(resource)
    db.commit()

    for od in request.order_details:
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            sandwich_id=od.sandwich_id,
            amount=od.amount
        )
        db.add(order_detail)
    db.commit()

    return new_order

def read_all(db: Session):
    return db.query(order_model.Order).all()

def read_one(db: Session, item_id: int):
    order = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def update(db: Session, item_id: int, request):
    order = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for var, value in vars(request).items():
        if value is not None:
            setattr(order, var, value)
    db.commit()
    db.refresh(order)
    return order

def delete(db: Session, item_id: int):
    order = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}

def get_orders_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(order_model.Order).filter(order_model.Order.order_date >= start_date, order_model.Order.order_date <= end_date).all()

def calculate_revenue_by_date(db: Session, target_date: datetime):
    from sqlalchemy.sql import cast, Date
    orders_on_date = db.query(order_model.Order).filter(
        cast(order_model.Order.order_date, Date) == target_date.date(),
        order_model.Order.status != "cancelled"
    ).all()

    total_revenue = 0.0
    for order in orders_on_date:
        for detail in order.order_details:
            sandwich_price = float(detail.sandwich.price)
            total_revenue += sandwich_price * detail.amount
    return {"date": target_date.date(), "total_revenue": total_revenue}

def get_order_by_tracking(db: Session, tracking_number: str):
    order = db.query(order_model.Order).filter(order_model.Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
