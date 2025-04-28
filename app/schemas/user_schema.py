from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel


class UserCreate(BaseModel):
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
    email: EmailStr
    password: Annotated[
        str,
        Field(min_length=8, description="Password must be at least 8 characters long."),
    ]
    full_name: Annotated[
        Optional[str],
        Field(default=None, description="Optional full name of the user."),
    ]
