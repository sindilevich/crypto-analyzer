from datetime import datetime, timezone
import uuid

from motor.motor_asyncio import AsyncIOMotorCollection


class TradeService:
    """
    TradeService class to handle trade-related operations.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_trade(self, trade_data: dict) -> dict:
        """
        Create a new trade in the database.
        Args:
            trade_data (dict): The trade data to create.
        Returns:
            dict: The created trade data.
        """

        trade_data["id"] = str(uuid.uuid4())
        trade_data["timestamp"] = datetime.now(tz=timezone.utc).timestamp()
        await self.collection.insert_one(trade_data)
        return trade_data

    async def get_trades_by_user(self, user_id: str) -> list:
        """
        Get all trades for a specific user.
        Args:
            user_id (str): The ID of the user.
        Returns:
            list: A list of trades for the user.
        """

        trades = await self.collection.find({"user_id": user_id}).to_list(length=None)
        return trades
