from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_session
from app.services.user import UserService
from app.db.models import User

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_user_service(session: SessionDep):
    return UserService(session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]