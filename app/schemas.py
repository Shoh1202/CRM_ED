from pydantic import BaseModel, ConfigDict, Field

class ClientCreate(BaseModel):
    name: str = Field(min_length=1)
    company: str
    city: str


class ClientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    company: str
    city: str

class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    company: str | None = None
    city: str | None = None


class TaskCreate(BaseModel):
    client_id:int
    title:str=Field(min_length=1)

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    client_id:int
    title:str
    done: bool

class DealCreate(BaseModel):
    client_id:int
    status:str=Field(min_length=1)
    amount:int
class DealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    client_id:int
    status:str=Field(min_length=1)
    amount:int

class DealStatusUpdate(BaseModel):
    status: str = Field(min_length=1)