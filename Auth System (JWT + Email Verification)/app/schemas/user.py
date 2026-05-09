from pydantic import BaseModel, EmailStr
from uuid import UUID

class BaseUser(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseUser):
    username: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    id: UUID
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str