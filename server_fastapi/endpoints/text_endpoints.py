from fastapi import APIRouter
from starlette import status

from core.logger import get_logger
from workers.tasks.celery_schema import HRRequirementsSchema
from workers.tasks.resume_task import resume_processing

reports_router = APIRouter(prefix="/resume", tags=["Resume"])

logger = get_logger("server-fastapi")


@reports_router.post("/v1", status_code=status.HTTP_202_ACCEPTED)
async def get_resume(token: str, hr_requirements: HRRequirementsSchema, resume: str):  # вот тут добавить следует
    # функция проверки токена
    result = resume_processing.delay(hr_requirements.model_dump(), resume)
    return {"detail": "Резюме в обработке, ожидайте", "task_id": result.id}
