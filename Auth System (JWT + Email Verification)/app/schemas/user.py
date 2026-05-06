from pydantic import BaseModel, EmailStr
from uuid import UUID

class BaseUser(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseUser):
    username: str

class UserLogin(BaseUser):
    pass

class UserRead(BaseModel):
    id: UUID
    email: EmailStr

class LoginResponse(BaseModel):
    id: UUID
    email: EmailStr
    token: str
    type: str