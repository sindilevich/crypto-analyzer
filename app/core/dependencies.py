from app.config import get_app_settings
from app.core.jwt_service import JwtService


def get_jwt_service():
    """
    Get the JWTService instance.
    Returns:
        JwtService: The JWTService instance.
    """

    return JwtService(get_app_settings())
