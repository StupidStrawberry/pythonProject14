from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Query
from models import Polzovatel, Feedback, CalculateRequest, UserCreate

app = FastAPI()


@app.get("/")
async def read():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/calculate")
async def calculate(data: CalculateRequest):
    result = data.num1 + data.num2
    return {"result": result}


@app.get("/users")
async def det_user():
    return Polzovatel


@app.post("/user")
async def det_user(data: Polzovatel):
    if data.age < 18:
        return {"name":data.name, "age":data.age}
    else:
        return {"name": data.name, "age": data.age, "is_adult": "true"}


@app.post("/feedback")
async def det_user(data: Feedback):
    name = data.name
    thanks = "Feedback received. Thank you, " + name + "!"
    file = open("feedback.txt", "a")
    file.write(data.name + ":" + data.message + "\n")
    file.close()
    return {"message": thanks}


@app.post("/create_user")
async def det_user(data: UserCreate):
    result = {"name": data.name, "email": data.email}
    if data.age is not None:
        result.update({"age": data.age})
    if data.is_subscribed is not None:
        result.update({"is_subscribed": data.is_subscribed})
    return result
