from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.db.models import User
from app.core.security import hash_password, verify_password, create_token
from sqlalchemy import select
from fastapi import status, HTTPException

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, create_user: UserCreate) -> User:
        user = User(
            username=create_user.username,
            email=create_user.email,
            password_hash=hash_password(create_user.password)
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def token(self, email: str, password: str):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        result = await self.session.execute(select(User).where(User.email == email))  # type: ignore
        user = result.scalar()

        if user is None:
            raise credentials_exception
        
        try:
            password_is_correct = verify_password(password, user.password_hash)
        
        except Exception:
            raise credentials_exception
        
        if not password_is_correct:
            raise credentials_exception
        
        token = create_token(
            data={
                "user":{
                    "name":user.username,
                    "id":str(user.id),
                }
            }
        )

        return user, token
