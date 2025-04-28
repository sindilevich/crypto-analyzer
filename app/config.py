from functools import lru_cache

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    AppSettings class for managing application settings.
    This class uses Pydantic to load settings from environment variables or a .env file.
    """

    model_config = {"env_file": "app/.env", "env_file_encoding": "utf-8"}

    access_token_secret: str
    access_token_algorithm: str
    access_token_expires_in_minutes: int

    mongodb_uri: str
    mongodb_db: str
    mongodb_users_collection: str


@lru_cache
def get_settings():
    """
    Get the application settings.
    Returns:
        AppSettings: The application settings.
    """

    return AppSettings()
