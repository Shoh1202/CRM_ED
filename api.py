import asyncio
import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()

clients = {
    1: {"id": 1, "name": "Анна", "company": "Ромашка", "city": "Москва"},
    2: {"id": 2, "name": "Борис", "company": "Вектор", "city": "Казань"},
    3: {"id": 3, "name": "Вера", "company": "Лотос", "city": "Москва"},
}
@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/clients/{client_id}")
async def get_client(client_id: int):
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return clients[client_id]
@app.get("/about")
async def get_about():
    return {"name": "Тестовый агент", "version": "01"}

@app.get("/clients")
async def list_clients(city: str | None = None,company: str |None=None, limit: int = 10):
    result = list(clients.values())
    if city is not None:
        result = [c for c in result if c["city"] == city]
    if company is not None:
        result = [c for c in result if c["company"] == company]
    return result[:limit]
class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    company: str
    city: str


@app.post("/clients", status_code=201)
async def create_client(data: ClientCreate):
    new_id = max(clients, default=0) + 1
    client = {"id": new_id, **data.model_dump()}
    clients[new_id] = client
    return client   

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    result = list(tasks.values())
    result = [t for t in result if t["client_id"] == client_id and not t["done"]]
    if result:
        raise HTTPException(status_code=409, detail="У клиента есть невыполненные задачи, удалять его нельзя")
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Клиент не найден") 
    del clients[client_id]
    return {"deleted": client_id}   
tasks = {}
class TaskCreate(BaseModel):
    client_id: int
    title: str = Field(min_length=1)

@app.post("/tasks",status_code=201)
async def create_task(data: TaskCreate):
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    new_id = max(tasks, default=0) + 1
    task = {"id": new_id, **data.model_dump(), "done": False}
    tasks[new_id] = task
    return task
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return tasks[task_id]    

@app.get("/tasks")
async def list_tasks(client_id:int | None=None, done:bool | None = None):
    result = list(tasks.values())
    if client_id is not None:
        result = [c for c in result if c["client_id"] == client_id]
    if done is not None:
        result = [c for c in result if c["done"] == done]    
    return result

@app.patch("/tasks/{task_id}/done")
async def task_patch (task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    tasks[task_id]["done"] = True
    return tasks[task_id]
@app.get("/clients/{client_id}/tasks")
async def get_client_tasks(client_id:int):
    result = list(tasks.values())
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    result = [c for c in result if c["client_id"] == client_id]
    return result   

@app.get("/wait-good")
async def wait_good():
    await asyncio.sleep(10)
    return {"done": True}


@app.get("/wait-bad")
async def wait_bad():
    time.sleep(10)
    return {"done": True}  

async def fake_model(text: str):
    for word in text.split():
        yield word + " "
        await asyncio.sleep(0.3)


@app.get("/stream")
async def stream():
    return StreamingResponse(
        fake_model("Hello from the streaming agent"),
        media_type="text/plain; charset=utf-8",
    )
    