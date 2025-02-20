from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, HTTPException, Cookie
from models import Polzovatel, Feedback, CalculateRequest, UserCreate, Product
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()


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


@app.post("/user")
async def post_user(data: Polzovatel):
    if data.age < 18:
        return {"name":data.name, "age":data.age}
    else:
        return {"name": data.name, "age": data.age, "is_adult": "true"}


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


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product



