from typing import Annotated

from pydantic import BaseModel, StringConstraints


class HRRequirementsSchema(BaseModel):
    vacancy_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
    years_of_work: int
    format_of_the_work: list[str]
    requirements: list[str]
    extra_requirements: list[str] | None
    tasks: list[str] | None


class ShowOneVacancySchema(BaseModel):
    vacancy_name: str
