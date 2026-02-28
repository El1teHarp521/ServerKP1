from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


class UserResponse(BaseModel):
    message: str
    user: User


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
