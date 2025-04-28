from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import AppSettings


class JwtService:
    """
    JwtService class for creating and verifying JWT tokens.
    This class uses the Jose library to handle JWT encoding and decoding.
    It requires the access token secret, algorithm, and expiration time to be set in the application settings.
    """

    def __init__(self, app_config: AppSettings):
        self.app_config = app_config

    def create_access_token(self, data: dict):
        """
        Create a JWT access token.
        Args:
            data (dict): The data to include in the token.
        Returns:
            str: The generated JWT access token.
        """

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.app_config.access_token_expires_in_minutes
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.app_config.access_token_secret,
            algorithm=self.app_config.access_token_algorithm,
        )
        return encoded_jwt
