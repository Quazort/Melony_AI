from fastapi import APIRouter
from core.logger import get_logger

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

logger = get_logger("server-fastapi")


@auth_router.post("/login")
async def user_login(a: str, psw: str):
    pass
    return "допилю проверку"


@auth_router.post("/registration")
async def user_registration(a: str, psw: str, email: str):
    pass
    return "потом"
