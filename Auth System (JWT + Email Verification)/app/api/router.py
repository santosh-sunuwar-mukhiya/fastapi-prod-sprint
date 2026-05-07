from fastapi import APIRouter
from app.api.routers.user import router as user_router
from app.api.routers.auth import router as auth_router

master_router = APIRouter()

master_router.include_router(user_router)
master_router.include_router(auth_router)