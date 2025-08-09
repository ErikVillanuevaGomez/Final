from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

@router.post("/", response_model=schema.Order)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Order])
def read_all_orders(db: Session = Depends(get_db), start_date: datetime | None = Query(default=None), end_date: datetime | None = Query(default=None)):
    if start_date and end_date:
        return controller.get_orders_by_date_range(db=db, start_date=start_date, end_date=end_date)
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Order)
def read_order(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Order)
def update_order(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete_order(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/revenue/{target_date}")
def get_revenue(target_date: datetime, db: Session = Depends(get_db)):
    return controller.calculate_revenue_by_date(db=db, target_date=target_date)

@router.get("/track/{tracking_number}", response_model=schema.Order)
def track_order(tracking_number: str, db: Session = Depends(get_db)):
    return controller.get_order_by_tracking(db=db, tracking_number=tracking_number)
