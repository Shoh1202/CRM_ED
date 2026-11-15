from fastapi import Depends, HTTPException, APIRouter
from app.database import get_db   
from app.schemas import DealCreate, DealOut, DealStatusUpdate
from app.models import Deal, Client, Task
from sqlalchemy.orm import Session
from sqlalchemy import select
router = APIRouter()

@router.post("/deals",status_code=201, response_model=DealOut)    
def create_deal(data:DealCreate, db: Session = Depends(get_db)):
    if db.get(Client, data.client_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    deal=Deal(**data.model_dump())
    db.add(deal)    
    db.commit()
    db.refresh(deal)
    return deal

@router.get("/deal/{client_id}", response_model=list[DealOut])
def get_deal(client_id: int, db: Session = Depends(get_db)):
    query=select(Deal).where(Deal.client_id==client_id)
    if db.get(Client, client_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return db.scalars(query).all()

@router.patch("/deals/{deal_id}/status", response_model=DealOut)
def patch_deal(deal_id:int, data: DealStatusUpdate, db: Session = Depends(get_db)):   
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Сделка не найдена")
    deal.status = data.status  
    db.commit()
    db.refresh(deal)
    return deal