from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey
from server_fastapi.database.models.base import Base


class ResumesModel(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    result: Mapped[dict] = mapped_column(JSON)

    vacancy: Mapped["VacanciesModel"] = relationship(back_populates="resume")