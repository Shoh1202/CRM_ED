# Точка входа: создаёт app = FastAPI(), таблицы и подключает роутеры.
# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import clients, tasks, deals

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(deals.router)