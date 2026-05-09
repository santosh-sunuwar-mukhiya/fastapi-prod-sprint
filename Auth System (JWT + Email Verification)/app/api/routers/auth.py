from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest, UserRead, UserCreate, LoginResponse
from typing import Annotated
from app.api.dependencies import UserDep, UserServiceDep, get_access_token
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["Auth"])

@router.post("/SignUp", response_model=UserRead)
async def register_user(service: UserServiceDep, user_create: UserCreate):
    return await service.add(user_create)

@router.post("/Login", response_model=LoginResponse)
async def login_user(service: UserServiceDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user,token = await service.token(form_data.username, form_data.password)

    return {
        "access_token": token,
        "token_type": "bearer",
        "id": user.id,
        "email": user.email
    }

@router.post("/logout")
async def logout(
    token_data: Annotated[dict, Depends(get_access_token)]
):
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
    user: UserDep,
    service: UserServiceDep,
    data: ResetPasswordRequest
):
    return await service.reset_password(
        data.token,
        data.new_password
    )