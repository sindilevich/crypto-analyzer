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
        expire = self.__calculate_expire()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.app_config.access_token_secret,
            algorithm=self.app_config.access_token_algorithm,
        )
        return encoded_jwt

    def verify_access_token(self, token: str):
        """
        Verify a JWT access token.
        Args:
            token (str): The JWT access token to verify.
        Returns:
            dict: The decoded data from the token if valid.
        Raises:
            ValueError: If the token is invalid or expired.
        """

        try:
            payload = jwt.decode(
                token,
                self.app_config.access_token_secret,
                algorithms=[self.app_config.access_token_algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            raise ValueError("Token has expired") from e
        except jwt.JWTClaimsError as e:
            raise ValueError("Invalid claims") from e
        except jwt.JWTError as e:
            raise ValueError("Invalid token") from e

    def __calculate_expire(self):
        """
        Calculate the expiration time for the JWT token.
        The expiration time is set to the current time plus the configured expiration time in minutes.
        The expiration time is rounded to the next minute.
        Returns:
            datetime: The expiration time for the JWT token.
        """

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.app_config.access_token_expires_in_minutes
        )

        # Round the expiration time to the next minute
        expire = expire.replace(second=0, microsecond=0) + timedelta(minutes=1)
        return expire
