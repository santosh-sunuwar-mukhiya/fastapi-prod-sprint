from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from app.db.session import get_session
from app.services.user import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import JWTError
from app.core.security import decode_token
from sqlalchemy import select
from app.db.models import User
from uuid import UUID
from app.db.redis import is_jti_blacklisted
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/Login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep):
    return UserService(session)

async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) ->dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired JWT Login Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, token_type="access")
        
        # Verify token type
        if payload.get("type") != "access":
            raise credentials_exception
            
        if await is_jti_blacklisted(payload["jti"]):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return payload

async def get_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Get refresh token from Authorization header"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired Refresh Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, token_type="refresh")
        
        # Verify token type
        if payload.get("type") != "refresh":
            logger.warning("Token type mismatch: expected 'refresh', got '%s'", payload.get("type"))
            raise credentials_exception
            
        if await is_jti_blacklisted(payload["jti"]):
            logger.warning("Refresh token JTI is blacklisted")
            raise credentials_exception
    except JWTError as e:
        logger.error("JWT decode error for refresh token: %s", str(e))
        raise credentials_exception
    
    return payload

async def get_refresh_token_from_cookie(request: Request) -> dict:
    """Get refresh token from httpOnly cookie (invisible to user)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No refresh token found. Please login again.",
    )
    
    # Get refresh token from httpOnly cookie
    token = request.cookies.get("refresh_token")
    
    if not token:
        logger.warning("No refresh token cookie found")
        raise credentials_exception
    
    try:
        payload = decode_token(token, token_type="refresh")
        
        # Verify token type
        if payload.get("type") != "refresh":
            logger.warning("Cookie token type mismatch: expected 'refresh', got '%s'", payload.get("type"))
            raise credentials_exception
            
        if await is_jti_blacklisted(payload["jti"]):
            logger.warning("Refresh token JTI from cookie is blacklisted")
            raise credentials_exception
    except JWTError as e:
        logger.error("JWT decode error for refresh token cookie: %s", str(e))
        raise credentials_exception
    
    return payload

async def get_current_user(
    token_data: Annotated[dict, Depends(get_access_token)],
    session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:

        user_data = token_data.get("user")

        if user_data is None:
            raise credentials_exception

        user_id = user_data.get("id")

        if user_id is None:
            raise credentials_exception
        
        # Convert string back to UUID
        user_id = UUID(user_id)

    except JWTError:
        raise credentials_exception

    result = await session.execute(
        select(User).where(User.id == user_id) # type: ignore
    )

    user = result.scalar()

    if user is None:
        raise credentials_exception

    return user

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

UserDep = Annotated[User, Depends(get_current_user)]

RefreshTokenDep = Annotated[dict, Depends(get_refresh_token)]

# For cookie-based refresh (invisible to user)
RefreshTokenCookieDep = Annotated[dict, Depends(get_refresh_token_from_cookie)]