from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.logger import get_logger
from server_fastapi.endpoints.start.start import main_router
from server_fastapi.endpoints.user.auth import auth_router
from server_fastapi.endpoints.user.users import user_router
from server_fastapi.endpoints.vacancy.crud_vacancy import vacancy_router

logger = get_logger("server_fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI-Приложение готово к работе")
    yield
    logger.info("FastAPI-Приложение закончило работу")


app = FastAPI(title="MelanyAI", lifespan=lifespan)

app.include_router(main_router)
app.include_router(vacancy_router)
app.include_router(auth_router)
app.include_router(user_router)


