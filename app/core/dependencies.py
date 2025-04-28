import logging

from app.config import get_app_settings
from app.core.jwt_service import JwtService


def get_jwt_service():
    """
    Get the JWTService instance.
    Returns:
        JwtService: The JWTService instance.
    """

    return JwtService(get_app_settings())


def get_logger(name: str = "uvicorn.error"):
    """
    Get a logger instance.
    Args:
        name (str): The name of the logger.
        Defaults to "uvicorn.error". This is the default logger used by Uvicorn.
        The logger name can be changed to any other name as needed.
    Returns:
        logging.Logger: The logger instance.
    """

    return logging.getLogger(name)
