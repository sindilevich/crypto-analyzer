from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.auth_service import AuthService
from app.core.dependencies import get_auth_service
from app.db.mongo import get_trade_collection
from app.schemas.common_response_schema import ErrorDetail
from app.schemas.trade_schema import TradeCreate, TradeResponse
from app.services.trade_service import TradeService


router = APIRouter(prefix="/api/v1/trades", tags=["Trades"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def __get_trade_service():
    """
    Get the trade service.
    """

    return TradeService(get_trade_collection())


@router.get(
    "",
    response_model=list[TradeResponse],
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorDetail}},
)
async def list_trades(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    trade_service: Annotated[TradeService, Depends(__get_trade_service)],
):
    """
    List all trades for the current user.
    """

    try:
        user = auth_service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from e

    trades = await trade_service.get_trades_by_user(user["sub"])
    return trades


@router.post(
    "",
    response_model=TradeResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorDetail}},
)
async def place_trade(
    trade: TradeCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    trade_service: Annotated[TradeService, Depends(__get_trade_service)],
):
    """
    Place a trade.
    """

    trade_data = trade.model_dump()
    try:
        user = auth_service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from e

    trade_data["user_id"] = user["sub"]

    result = await trade_service.create_trade(trade_data)
    return result
