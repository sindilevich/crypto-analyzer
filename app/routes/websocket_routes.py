import logging
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.dependencies import get_jwt_service, get_logger
from app.core.jwt_service import JwtService

AUTHORIZATION_HEADER = "Authorization"
AUTHORIZATION_PREFIX = "Bearer "

router = APIRouter(prefix="/websocket/v1")


@router.websocket("/trade-stream")
async def websocket_endpoint(
    websocket: WebSocket,
    logger: Annotated[logging.Logger, Depends(get_logger)],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
):
    """
    WebSocket endpoint for trading stream.
    Args:
        websocket (WebSocket): The WebSocket connection.
    """

    await websocket.accept()

    token = websocket.headers.get(AUTHORIZATION_HEADER)

    if not token or not token.startswith(AUTHORIZATION_PREFIX):
        await websocket.close(code=1008)
        return
    token = token[len(AUTHORIZATION_PREFIX) :].strip()
    if not token:
        await websocket.close(code=1008)
        return

    try:
        user = jwt_service.verify_access_token(token)
    except ValueError as e:
        logger.error("Token verification failed: %s", str(e))
        await websocket.close(code=1008)
        return

    if not user:
        await websocket.close(code=1008)
        return

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Hello {user['sub']}, you sent: {data}")
    except WebSocketDisconnect:
        logger.info("Client [%s] disconnected", user["sub"])
    finally:
        logger.info("Closing WebSocket connection")
