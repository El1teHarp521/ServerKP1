from pydantic import BaseModel


class User(BaseModel):
    username: str
    user_info: str


class UserResponse(BaseModel):
    username: str
    user_info: str
    status: str = "active"
