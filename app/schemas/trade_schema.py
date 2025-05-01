from enum import Enum

from pydantic import AliasGenerator, BaseModel, Field
from pydantic.alias_generators import to_camel


class TradeAction(str, Enum):
    """
    Enum for trade actions.
    """

    BUY = "buy"
    SELL = "sell"


class TradeCreate(BaseModel):
    """
    Schema for creating a trade.
    """

    model_config = {
        "alias_generator": AliasGenerator(
            serialization_alias=to_camel,
        )
    }

    action: TradeAction
    amount: float = Field(..., gt=0, description="Amount of the trade")
    price: float = Field(..., gt=0, description="Price of the trade")
    symbol: str = Field(..., examples=["AAPL", "GOOGL"])


class TradeResponse(TradeCreate):
    """
    Schema for trade response.
    """

    id: str = Field(..., description="ID of the trade")
    user_id: str = Field(..., description="ID of the user who made the trade")
    timestamp: float = Field(..., description="Timestamp of the trade")
