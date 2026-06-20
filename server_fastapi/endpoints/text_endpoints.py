from fastapi import APIRouter
from starlette import status

from core.logger import get_logger
from workers.tasks.resume_task import resume_processing

reports_router = APIRouter(prefix="/resume", tags=["Resume"])

logger = get_logger("server-fastapi")


@reports_router.post("/v1", status_code=status.HTTP_202_ACCEPTED)
async def get_resume(token: str, resume: str):
    # TODO - Основная логика обработки резюме
    return {"detail": "Резюме в обработке, ожидайте"}
