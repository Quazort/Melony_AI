from fastapi import APIRouter
from core.logger import get_logger

vacancy_router = APIRouter(prefix="/vacancy", tags=["Vacancy"])

logger = get_logger("server-fastapi")


@vacancy_router.post("")
async def vacancy_create(a: str):
    pass
    return 'dddd'


@vacancy_router.delete("/{vacancy_id}")
async def vacancy_delete(a: str):
    pass
    return 'dddd'


@vacancy_router.put("/{vacancy_id}")
async def vacancy_edit(a: str):
    pass
    return 'dddd'


@vacancy_router.get("/{vacancy_id}")
async def vacancy_get_one(a: str):
    pass
    return 'dddd'


@vacancy_router.get("")
async def get_all_vacancies(a: str):
    pass
    return 'dddd'
