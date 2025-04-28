import os

from fastapi import FastAPI, WebSocket

from app.routes import auth

app = FastAPI(
    title="Crypto Trading Bot",
    description="A trading bot for cryptocurrency exchanges",
    version="0.1.0",
)

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Crypto World!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello WebSocket World!")
    await websocket.close()
