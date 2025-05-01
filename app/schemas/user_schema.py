from typing import Annotated, Optional

from pydantic import AliasGenerator, BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel


class UserLogin(BaseModel):
    """
    UserLogin schema for user login.
    This schema is used to validate the data when a user attempts to log in.
    """

    model_config = {
        "alias_generator": to_camel,
    }

    username: Annotated[
        str,
        Field(
            min_length=4,
            max_length=20,
            pattern=r"^\w+$",
            description="Username must be 4-20 characters long and can only contain letters, numbers, and underscores.",
        ),
    ]
    password: Annotated[
        str,
        Field(min_length=8, description="Password must be at least 8 characters long."),
    ]


class UserLoginResponse(BaseModel):
    """
    UserLoginResponse schema for user login response.
    This schema is used to validate the data returned when a user logs in successfully.
    """

    access_token: str
    token_type: str


class UserCreate(UserLogin):
    """
    UserCreate schema for creating a new user.
    This schema is used to validate the data when creating a new user.
    """

    email: EmailStr
    full_name: Annotated[
        Optional[str],
        Field(default=None, description="Optional full name of the user."),
    ]
