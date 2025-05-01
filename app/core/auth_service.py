from app.core.jwt_service import JwtService


class AuthService:
    """
    AuthService is responsible for handling authentication-related tasks.
    It uses the JwtService to verify and decode JWT tokens.
    """

    def __init__(self, jwt_service: JwtService):
        self.jwt_service = jwt_service

    def get_current_user(self, token: str):
        """
        Get the current user from the JWT access token.
        Args:
            token (str): The JWT access token.
        Returns:
            dict: The decoded data from the token if valid.
        Raises:
            ValueError: If the token is invalid or expired.
        """

        payload = self.jwt_service.verify_access_token(token)

        if not payload:
            raise ValueError("Invalid token")
        return payload
