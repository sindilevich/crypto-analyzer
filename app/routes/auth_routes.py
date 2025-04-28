from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user_schema import UserCreate
from app.services.user_service import DuplicateUserError, UserService

router = APIRouter(prefix="/api/v1")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, user_service: Annotated[UserService, Depends(UserService)]
):
    """
    Register a new user.
    Args:
        user (UserCreate): The user data to register.
        user_service (UserService): The UserService instance.
    Returns:
        dict: A message indicating successful registration.
    Raises:
        HTTPException: If a user with the same username or email already exists.
    """
    try:
        await user_service.create_user(user)
        return {"message": f"User {user.username} registered successfully"}
    except DuplicateUserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
