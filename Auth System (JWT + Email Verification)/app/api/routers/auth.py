from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest, UserRead, UserCreate, UserLogin, LoginResponse
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

@router.post("/logout")
async def logout():
    return {
        "message": "Frontend should delete token"
    }

@router.post("/forgot-password")
async def forgot_password(
    service: UserServiceDep,
    data: ForgotPasswordRequest
):
    return await service.create_reset_token(data.email)


@router.post("/reset-password")
async def reset_password(
    service: UserServiceDep,
    data: ResetPasswordRequest
):
    return await service.reset_password(
        data.token,
        data.new_password
    )