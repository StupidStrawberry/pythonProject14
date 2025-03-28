from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, create_todo, get_todo, update_todo, delete_todo, get_all_todos
from models import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(todo: TodoCreate):
    return await create_todo(todo)

@app.get("/todos", response_model=TodoListResponse)
async def get_all_todos_endpoint():
    return {"todos": await get_all_todos()}

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo_endpoint(todo_id: int):
    todo = await get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo_endpoint(todo_id: int, todo: TodoUpdate):
    updated = await update_todo(todo_id, todo)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(todo_id: int):
    if not await delete_todo(todo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")