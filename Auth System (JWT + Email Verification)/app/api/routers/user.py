from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.db.models import User
from typing import Annotated 

router = APIRouter(prefix="/profile", tags=["User"])

@router.get("/me")
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }