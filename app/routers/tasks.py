from fastapi import Depends, HTTPException, APIRouter
from app.database import get_db   
from app.schemas import TaskCreate, TaskOut
from app.models import Deal, Client, Task
from sqlalchemy.orm import Session
from sqlalchemy import select
router = APIRouter()

@router.post("/tasks",status_code=201, response_model=TaskOut)    
def create_task(data:TaskCreate, db: Session = Depends(get_db)):
    if db.get(Client, data.client_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    task=Task(**data.model_dump())
    db.add(task)    
    db.commit()
    db.refresh(task)
    return task

@router.patch("/tasks/{task_id}/done", response_model=TaskOut)
def patch_task(task_id:int,  db: Session = Depends(get_db)):   
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="задача не найдена")
    task.done = True
    db.commit()
    db.refresh(task)
    return task    

@router.get("/clients/{client_id}/tasks",response_model=list[TaskOut])
def get_task(client_id: int, db: Session = Depends(get_db)):
    if db.get(Client, client_id) is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    query=select(Task).where(Task.client_id==client_id)
    return db.scalars(query).all()
    