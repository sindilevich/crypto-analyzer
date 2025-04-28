from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Error details schema for API responses.
    """

    detail: str


class Message(BaseModel):
    """
    Message schema for API responses.
    """

    message: str
