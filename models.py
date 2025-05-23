from pydantic import BaseModel
from typing import Optional, List

# Модели для запросов
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Модели для ответов API
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

class TodoListResponse(BaseModel):
    todos: List[TodoResponse]