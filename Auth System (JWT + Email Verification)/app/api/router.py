from fastapi import APIRouter
from app.api.routers.user import router
from app.api.routers.auth import router

master_router = APIRouter()

master_router.include_router(router)
master_router.include_router(router)