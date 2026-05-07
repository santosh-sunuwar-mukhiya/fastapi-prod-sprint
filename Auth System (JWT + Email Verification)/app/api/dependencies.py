from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_session
from app.services.user import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import JWTError
from app.core.security import decode_token
from sqlalchemy import select
from app.db.models import User
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/Login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep):
    return UserService(session)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)

        user_data = payload.get("user")

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
        select(User).where(User.id == user_id)
    )

    user = result.scalar()

    if user is None:
        raise credentials_exception

    return user

UserServiceDep = Annotated[UserService, Depends(get_user_service)]