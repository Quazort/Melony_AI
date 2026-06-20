from celery import Celery

from core.config import settings

app = Celery("My_tasks",
             broker=settings.REDIS_BROKER_URL,
             backend=settings.REDIS_BACKEND_URL,
             include=["workers.tasks.resume_task"],)
