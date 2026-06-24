from pydantic import BaseModel


class ResponseAISchema(BaseModel):
    full_name: str
    date_of_birth: str
    years_of_work: list[int]
    format_of_the_work: list[str]
    skills: list[str]
    extra_skills: list[str]
    matching_tasks: list[str]
    strengths: list[str]
    weaknesses: list[str]


class ResponseSchema(BaseModel):
    full_name: str
    date_of_birth: str
    points: float
    years_of_work: list[int]
    format_of_the_work: list[str]
    skills: list[str]
    extra_skills: list[str]
    matching_tasks: list[str]
    strengths: list[str]
    weaknesses: list[str]


class HRRequirementsSchema(BaseModel):
    vacancy_name: str
    years_of_work: int
    format_of_the_work: list[str]
    requirements: list[str]
    extra_requirements: list[str] | None
    tasks: list[str] | None
