from fastapi import FastAPI

from app.routes import auth_routes, trade_routes, websocket_routes


app = FastAPI(
    title="Crypto Trading Bot",
    description="A trading bot for cryptocurrency exchanges",
    version="0.1.0",
)

app.include_router(auth_routes.router)
app.include_router(trade_routes.router)
app.include_router(websocket_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello Crypto World!"}
