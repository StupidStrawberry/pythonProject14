from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from models import Polzovatel

app = FastAPI()


@app.get("/")
async def read():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


class CalculateRequest(BaseModel):
    num1: int
    num2: int


class User(BaseModel):
    name: str
    age: int



@app.post("/calculate")
async def calculate(data: CalculateRequest):
    result = data.num1 + data.num2
    return {"result": result}


@app.get("/users")
async def det_user():
    return User


@app.post("/user")
async def det_user(data: User):
    if data.age < 18:
        return {"name":data.name, "age":data.age}
    else:
        return {"name": data.name, "age": data.age, "is_adult": "true"}
