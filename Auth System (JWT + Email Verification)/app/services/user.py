from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.db.models import User
from app.core.security import decode_token, hash_password, verify_password, create_token
from sqlalchemy import select
from fastapi import status, HTTPException

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, create_user: UserCreate) -> User:
        existing_user = await self.session.execute(
            select(User).where(User.email == create_user.email) # type: ignore
        )

        if existing_user.scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "Email already Exists."
            )

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
    
    async def create_reset_token(self, email: str):
        result = await self.session.execute(
            select(User).where(User.email == email) # type: ignore
        )

        user = result.scalar()

        if user is None:
            raise HTTPException(404, "User not found")

        token = create_token(
            data={
                "reset_password": str(user.id)
            }
        )

        print(
            f"http://localhost:8000/user/reset-password?token={token}"
        )

        return {
            "message": "Reset link sent"
        }

    async def reset_password(
        self,
        token: str,
        new_password: str
    ):
        try:
            payload = decode_token(token)
            user_id = payload.get("reset_password")

            if user_id is None:
                raise HTTPException(400, "Invalid token")

        except Exception:
            raise HTTPException(400, "Invalid token")

        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar()

        if user is None:
            raise HTTPException(404, "User not found")

        user.password_hash = hash_password(new_password)

        await self.session.commit()

        return {
            "message": "Password updated successfully"
        }
        
