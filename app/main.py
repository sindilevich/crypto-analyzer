import os

from fastapi import FastAPI, WebSocket

from app.routes import auth_routes

app = FastAPI(
    title="Crypto Trading Bot",
    description="A trading bot for cryptocurrency exchanges",
    version="0.1.0",
)

app.include_router(auth_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello Crypto World!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello WebSocket World!")
    await websocket.close()
