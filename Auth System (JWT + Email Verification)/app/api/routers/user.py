from app.schemas.user import UserRead
from app.api.dependencies import UserServiceDep
from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])

# User profile endpoints
# @router.get("/me", response_model=UserRead)
# async def get_current_user(current_user):
#     return current_user

# @router.put("/me", response_model=UserRead)
# async def update_profile(current_user, updates):
#     # Update user profile logic
#     pass

# @router.delete("/me")
# async def delete_account(current_user):
#     # Delete user logic
#     pass
