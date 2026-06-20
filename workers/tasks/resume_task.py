from core.logger import get_logger
from workers.tasks.general_agent import Agent
from workers.celery_config import app

logger = get_logger("celery-worker")


@app.task(name="resume_task")
def resume_processing(text):
    # TODO: Тут будет полный пайплайн
    return "SUCCESS"
