import uuid
import re
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, HTTPException, Depends, Response, status, Request
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from models import Polzovatel, Feedback, CalculateRequest, UserCreate, Product, UserLogin
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

"""
sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

"""
sessions = {}

# Временное хранилище для пользователей
users = {
    "user123": {
        "password": "password123",
        "email": "user123@example.com"
    }
}

security = HTTPBasic()

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
async def get_user():
    return Polzovatel

"""
@app.post("/user")
async def post_user(data: Polzovatel):
    if data.age < 18:
        return {"name":data.name, "age":data.age}
    else:
        return {"name": data.name, "age": data.age, "is_adult": "true"}
"""

@app.post("/feedback")
async def feedback(data: Feedback):
    name = data.name
    thanks = "Feedback received. Thank you, " + name + "!"
    file = open("feedback.txt", "a")
    file.write(data.name + ":" + data.message + "\n")
    file.close()
    return {"message": thanks}


@app.post("/create_user")
async def create_user(data: UserCreate):
    result = {"name": data.name, "email": data.email}
    if data.age is not None:
        result.update({"age": data.age})
    if data.is_subscribed is not None:
        result.update({"is_subscribed": data.is_subscribed})
    return result


class ProductSearchRequest(BaseModel):
    keyword: str
    category: Optional[str] = None
    limit: Optional[int] = 10

"""
@app.get("/products/search")
async def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: Optional[int] = Query(10, gt=0)
):
    results = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category and product["category"].lower() != category.lower():
                continue
            results.append(product)
            if len(results) >= limit:
                break
    return results
"""
"""
@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
"""

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    if username in users and users[username]["password"] == password:
        return username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.get("/login")
async def login(username: str = Depends(authenticate_user), response: Response = None):
    session_token = str(uuid.uuid4())
    sessions[session_token] = username
    response.set_cookie(key="session_token", value=session_token, httponly=True, secure=True)

    return {"message": "You got my secret, welcome"}



@app.get("/user")
async def get_user_profile(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token in sessions:
        username = sessions[session_token]
        user_profile = users[username]
        return UserLogin(username=user_profile["username"], password=user_profile["password"])
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

ACCEPT_LANGUAGE_PATTERN = re.compile(r'^[a-zA-Z-]+(,[a-zA-Z-]+)*(;q=[0-9.]+)?(,[a-zA-Z-]+(;q=[0-9.]+)?)*$')

@app.get("/headers")
async def get_headers(request: Request):
    user_agent = request.headers.get("User-Agent")
    accept_language = request.headers.get("Accept-Language")
    if not user_agent or not accept_language:
        raise HTTPException(
            status_code=400,
            detail="Missing required headers: 'User-Agent' or 'Accept-Language'"
        )
    if not ACCEPT_LANGUAGE_PATTERN.match(accept_language):
        raise HTTPException(
            status_code=400,
            detail="Invalid 'Accept-Language' header format"
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }