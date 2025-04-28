from passlib.context import CryptContext

from app.db.mongo import get_user_collection
from app.schemas.user_schema import UserCreate


class DuplicateUserError(Exception):
    """Exception raised when a user with the same username or email already exists."""

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __str__(self):
        return f"User with username '{self.username}' or email '{self.email}' already registered"


class UserService:
    """Service for user-related operations."""


    async def create_user(self, user: UserCreate):
        """
        Create a new user in the database.
        Args:
            user (UserCreate): The user data to create.
        Returns:
            Any: The ID of the created user.
        Raises:
            DuplicateUserError: If a user with the same username or email already exists.
        """

        if await self.__check_user_exists(user.username, user.email):
            raise DuplicateUserError(user.username, user.email)

        hashed_password = self.__pwd_context.hash(user.password)
        user_doc = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password,
            "full_name": user.full_name,
        }
        result = await self.collection.insert_one(user_doc)

        return result.inserted_id

    async def __check_user_exists(self, username, email):
        """
        Check if a user with the given username or email already exists in the database.
        Args:
            username (str): The username to check.
            email (str): The email to check.
        Returns:
            bool: True if the user exists, False otherwise.
        """

        user = await self.collection.find_one(
            {"$or": [{"username": username}, {"email": email}]}
        )
        return user is not None
