import asyncio
import logging
import time
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.dependencies import get_jwt_service, get_logger
from app.core.jwt_service import JwtService

AUTHORIZATION_HEADER = "Authorization"
AUTHORIZATION_PREFIX = "Bearer "
MAX_QUEUE_SIZE = 10

router = APIRouter(prefix="/websocket/v1")


async def __consumer(
    websocket: WebSocket,
    logger: logging.Logger,
    message_queue: asyncio.Queue,
    user: dict,
):
    """
    Consumer function to process messages from the queue.
    Args:
        websocket (WebSocket): The WebSocket connection.
        logger (logging.Logger): The logger instance.
        message_queue (asyncio.Queue): The message queue.
        user (dict): The user information.
    """

    try:
        while True:
            message = await message_queue.get()
            await websocket.send_text(message)
    except WebSocketDisconnect:
        logger.info("Client [%s] disconnected (consumer)", user["sub"])
    except asyncio.CancelledError:
        pass


async def __producer(
    logger: logging.Logger,
    message_queue: asyncio.Queue,
    user: dict,
):
    """
    Producer function to send messages to the queue.
    Args:
        logger (logging.Logger): The logger instance.
        message_queue (asyncio.Queue): The message queue.
        user (dict): The user information.
    """

    try:
        while True:
            await asyncio.sleep(0.5)
            data = f"Message from producer to client [{user['sub']}] at {time.time()}"

            if message_queue.full():
                logger.warning("Queue is full, dropping message")
                # Drop the oldest message
                _ = await message_queue.get_nowait()
            await message_queue.put(data)
    except asyncio.CancelledError:
        pass


def __try_authenticate(
    jwt_service: JwtService,
    logger: logging.Logger,
    token: str,
) -> dict | None:
    """
    Helper function to authenticate the user using JWT token.
    Args:
        jwt_service (JwtService): The JWT service instance.
        logger (logging.Logger): The logger instance.
        token (str): The JWT token.
    Returns:
        dict: The user information if authentication is successful, None otherwise.
    """

    if not token or not token.startswith(AUTHORIZATION_PREFIX):
        return None
    token = token[len(AUTHORIZATION_PREFIX) :].strip()
    if not token:
        return None

    try:
        user = jwt_service.verify_access_token(token)
    except ValueError as e:
        logger.error("Token verification failed: %s", str(e))
        return None

    if not user:
        return None
    return user


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
    user = __try_authenticate(jwt_service, logger, token)

    if not user:
        await websocket.close(code=1008)
        return

    message_queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)
    consumer_task = asyncio.create_task(
        __consumer(websocket, logger, message_queue, user)
    )
    producer_task = asyncio.create_task(__producer(logger, message_queue, user))

    try:
        await asyncio.gather(consumer_task, producer_task)
    finally:
        consumer_task.cancel()
        producer_task.cancel()
