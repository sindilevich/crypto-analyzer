from functools import lru_cache

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    model_config = {"env_file": "app/.env", "env_file_encoding": "utf-8"}

    mongodb_uri: str
    mongodb_db: str
    mongodb_users_collection: str


@lru_cache
def get_settings():
    return AppSettings()
