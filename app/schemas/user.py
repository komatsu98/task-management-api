from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    employee = "employee"
    employer = "employer"


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
