from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext

from app.schemas.user_schema import UserCreate, UserLogin


class DuplicateUserError(Exception):
    """Exception raised when a user with the same username or email already exists."""

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __str__(self):
        return f"User with username '{self.username}' or email '{self.email}' already registered"


class UserService:
    """Service for user-related operations."""

    def __init__(self, collection: AsyncIOMotorCollection, pwd_context: CryptContext):
        self.collection = collection
        self.__pwd_context = pwd_context

    async def authenticate_user(self, user: UserLogin):
        """
        Authenticate a user by checking the username and password.
        Args:
            user (UserLogin): The user data to authenticate.
        Raises:
            ValueError: If the username or password is incorrect.
        """

        db_user = await self.collection.find_one({"username": user.username})

        if not db_user:
            raise ValueError("Incorrect username or password")

        if not self.__pwd_context.verify(user.password, db_user["password"]):
            raise ValueError("Incorrect username or password")

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
