from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = "mongodb://crypto-analyzer-mongodb:27017"
MONGODB_DB = "crypto_app"
USERS_COLLECTION = "users"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]


def get_user_collection():
    return db[USERS_COLLECTION]
