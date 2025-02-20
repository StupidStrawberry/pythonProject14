from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Polzovatel(BaseModel):
    name: str = Field(default=...)
    id: int = Field(default=...)


class Feedback(BaseModel):
    name: str = Field(default=...)
    message: str = Field(default=...)


class CalculateRequest(BaseModel):
    num1: int = Field(default=...)
    num2: int = Field(default=...)


class User(BaseModel):
    name: str = Field(default=...)
    age: int = Field(default=...)


class UserCreate(BaseModel):
    name: str = Field(default=...)
    email: EmailStr = Field(default=...)
    age: Optional[int] = Field(default=None, ge=1)
    is_subscribed: Optional[bool] = Field(default=None)


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
