from typing import Annotated

from pydantic import BaseModel, StringConstraints


class ShortResumeSchema(BaseModel):
    candidates_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
    vacancy_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]


class ResumeResponseAISchema(BaseModel):
    full_name: str
    date_of_birth: str
    years_of_work: list[int]
    format_of_the_work: list[str]
    skills: list[str]
    extra_skills: list[str]
    matching_tasks: list[str]
    strengths: list[str]
    weaknesses: list[str]


class ResumeResponseSchema(ResumeResponseAISchema):
    points: float
