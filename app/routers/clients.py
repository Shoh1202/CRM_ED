from fastapi import Depends, HTTPException, APIRouter
from app.database import get_db   
from app.schemas import ClientCreate, ClientOut, ClientUpdate
from app.models import Deal, Client, Task
from sqlalchemy.orm import Session
from sqlalchemy import select
router = APIRouter()

@router.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client


# Задание 1: POST /clients
@router.post("/clients", status_code=201, response_model=ClientOut)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**data.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)
    return client
    
# Задание 2: GET /clients с фильтром по городу
@router.get("/clients",response_model=list[ClientOut])
def get_clients(city: str | None = None, db: Session = Depends(get_db)):
    query = select(Client)
    if city is not None:
        query=query.where(Client.city==city)
        
    return db.scalars(query).all()


@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.get(Client,client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    task = db.scalars(select(Task).where(Task.client_id == client_id)).first()
    if task is not None:
        raise HTTPException(status_code=409, detail="У клиент есть задача")
    deal = db.scalars(select(Deal).where(Deal.client_id == client_id)).first()
    if deal is not None:
        raise HTTPException(status_code=409, detail="У клиент есть сделка")
    db.delete(client)
    db.commit()
    return {"deleted": client_id}
@router.patch("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int,data:ClientUpdate, db: Session = Depends(get_db)):
    client = db.get(Client, client_id)
    changes = data.model_dump(exclude_unset=True)
    if client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    for field, value in changes.items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


