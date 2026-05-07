from fastapi import APIRouter, Depends
from app.api.dependencies import UserDep

router = APIRouter(prefix="/profile", tags=["User"])

@router.get("/me")
async def me(current_user: UserDep):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }