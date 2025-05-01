from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from passlib.context import CryptContext

from app.core.dependencies import get_jwt_service
from app.core.jwt_service import JwtService
from app.db.mongo import get_user_collection
from app.schemas.common_response_schema import ErrorDetail, Message
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
)
from app.services.user_service import DuplicateUserError, UserService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


def __get_user_service():
    """
    Get the UserService instance.
    Returns:
        UserService: The UserService instance.
    """

    return UserService(
        get_user_collection(), CryptContext(schemes=["bcrypt"], deprecated="auto")
    )


@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorDetail}},
)
async def login_user(
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
    user_service: Annotated[UserService, Depends(__get_user_service)],
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Login a user and return a JWT token.
    Args:
        jwt_service (JwtService): The JWTService instance.
        user_service (UserService): The UserService instance.
        username (str): The username of the user.
        password (str): The password of the user.
    Returns:
        dict: A dictionary containing the JWT token.
    Raises:
        HTTPException: If the username or password is incorrect.
    """

    try:
        user = UserLogin(username=username, password=password)

        await user_service.authenticate_user(user)
        token = jwt_service.create_access_token(data={"sub": user.username})
        return UserLoginResponse(
            access_token=token,
            token_type="bearer",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorDetail}},
)
async def register_user(
    user: UserCreate, user_service: Annotated[UserService, Depends(__get_user_service)]
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
        return Message(message=f"User {user.username} registered successfully")
    except DuplicateUserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
