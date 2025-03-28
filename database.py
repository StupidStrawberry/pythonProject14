import asyncpg
from typing import Optional, List, Dict
from models import TodoCreate, TodoUpdate
import logging

logger = logging.getLogger(__name__)

pool: Optional[asyncpg.Pool] = None

async def init_db():
    global pool
    try:
        pool = await asyncpg.create_pool(
            "postgresql://postgres:postgres@localhost:5432/todo_db",
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE
                )
            """)
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

async def create_todo(todo: TodoCreate) -> Dict:
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            "INSERT INTO todos (title, description) VALUES ($1, $2) RETURNING *",
            todo.title, todo.description
        )
        return dict(record)

async def get_todo(todo_id: int) -> Optional[Dict]:
    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            "SELECT * FROM todos WHERE id = $1", todo_id
        )
        return dict(record) if record else None

async def get_all_todos() -> List[Dict]:
    async with pool.acquire() as conn:
        records = await conn.fetch("SELECT * FROM todos")
        return [dict(record) for record in records]

async def update_todo(todo_id: int, todo: TodoUpdate) -> Optional[Dict]:
    current = await get_todo(todo_id)
    if not current:
        return None

    update_data = {
        "title": todo.title if todo.title is not None else current["title"],
        "description": todo.description if todo.description is not None else current["description"],
        "completed": todo.completed if todo.completed is not None else current["completed"]
    }

    async with pool.acquire() as conn:
        record = await conn.fetchrow(
            """
            UPDATE todos SET
                title = $1,
                description = $2,
                completed = $3
            WHERE id = $4
            RETURNING *
            """,
            update_data["title"],
            update_data["description"],
            update_data["completed"],
            todo_id
        )
        return dict(record)

async def delete_todo(todo_id: int) -> bool:
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM todos WHERE id = $1", todo_id
        )
        return "DELETE 1" in result