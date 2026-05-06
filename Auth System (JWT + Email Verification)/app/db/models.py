from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from uuid import uuid4, UUID

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str 
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    is_verified: bool = False