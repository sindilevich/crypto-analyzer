from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.user_provider import DuplicateUserError, UserProvider
from app.schemas.user import UserCreate

router = APIRouter(prefix="/api/v1")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, users_provider: Annotated[UserProvider, Depends(UserProvider)]
):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to register.

    Returns:
        dict: A message indicating successful registration.
    """
    try:
        await users_provider.create_user(user)
        return {"message": f"User {user.username} registered successfully"}
    except DuplicateUserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
