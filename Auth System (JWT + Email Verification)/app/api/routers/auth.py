from app.schemas.user import UserRead, UserCreate, UserLogin, LoginResponse
# from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.dependencies import UserServiceDep
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/user", tags=["Auth"])

@router.post("/SignUp", response_model=UserRead)
async def register_user(service: UserServiceDep, user_create: UserCreate):
    return await service.add(user_create)

@router.post("/Login", response_model=LoginResponse)
async def login_user(service: UserServiceDep, request_form: Annotated[UserLogin, Depends()]):
    user, token = await service.token(
        request_form.email,
        request_form.password
    )   # UserLogin = used instead of OAuth2PasswordRequestForm

    return {
        "id": user.id,
        "email": user.email,
        "token": token,
        "type": "Bearer"
    }