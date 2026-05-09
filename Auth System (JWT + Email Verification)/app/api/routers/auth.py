from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest, UserRead, UserCreate, LoginResponse
from typing import Annotated
from app.api.dependencies import UserDep, UserServiceDep, get_access_token, RefreshTokenCookieDep
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.db.redis import add_jti_to_blacklist
from app.core.security import create_access_token

router = APIRouter(prefix="/user", tags=["Auth"])

@router.post("/SignUp", response_model=UserRead)
async def register_user(service: UserServiceDep, user_create: UserCreate):
    return await service.add(user_create)

@router.post("/Login", response_model=LoginResponse)
async def login_user(service: UserServiceDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    user, access_token, refresh_token = await service.token(form_data.username, form_data.password)

    # Set refresh token as httpOnly cookie (secure, invisible to user)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Not accessible via JavaScript
        secure=False,   # Set to True in production (HTTPS only)
        samesite="lax",  # CSRF protection
        max_age=7*24*60*60  # 7 days in seconds
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # Still return for documentation
        "token_type": "bearer",
        "id": user.id,
        "email": user.email
    }

@router.post("/refresh")
async def refresh_access_token(token_data: RefreshTokenCookieDep):
    """
    Get a new access token using refresh token from cookie (INVISIBLE to user).
    
    The client doesn't need to send Authorization header.
    The refresh token is automatically sent via httpOnly cookie.
    Frontend can call this when access token expires (handle 401 responses).
    """
    new_access_token = create_access_token(
        data={
            "user": token_data.get("user")
        }
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    token_data: Annotated[dict, Depends(get_access_token)],
    response: Response
):
    await add_jti_to_blacklist(token_data["jti"])
    
    # Clear refresh token cookie
    response.delete_cookie("refresh_token")
    
    return {
        "message": "Logged out successfully. Frontend should delete access token."
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