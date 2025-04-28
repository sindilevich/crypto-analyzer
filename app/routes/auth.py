from fastapi import APIRouter, status

from app.schemas.user import UserCreate

router = APIRouter(prefix="/api/v1")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    return {"message": "User registered successfully", "user": user}
