from motor.motor_asyncio import AsyncIOMotorClient

from app.core.dependencies import get_app_settings


app_settings = get_app_settings()

client = AsyncIOMotorClient(app_settings.mongodb_uri)
db = client[app_settings.mongodb_db]


def get_user_collection():
    """
    Get the user collection from the MongoDB database.
    Returns:
        AsyncIOMotorCollection: The user collection.
    """

    return db[app_settings.mongodb_users_collection]
