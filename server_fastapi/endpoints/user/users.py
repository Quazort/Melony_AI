from fastapi import APIRouter
from core.logger import get_logger

user_router = APIRouter(prefix="/users", tags=["User"])

logger = get_logger("server-fastapi")


@user_router.delete("/delete")
async def user_delete(a: str, psw: str, email: str):
    pass
    return "потом"
