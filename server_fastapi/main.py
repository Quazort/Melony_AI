from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.logger import get_logger
from server_fastapi.endpoints.text_endpoints import reports_router

logger = get_logger("server_fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI-Приложение готово к работе")
    yield
    logger.info("FastAPI-Приложение закончило работу")


app = FastAPI(title="MelanyAI", lifespan=lifespan)

app.include_router(reports_router)
