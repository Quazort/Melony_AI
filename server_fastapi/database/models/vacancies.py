from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server_fastapi.database.models.base import Base


class VacanciesModel(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    requirements: Mapped[dict] = mapped_column(JSON)

    user: Mapped["UsersModel"] = relationship(back_populates="vacancies")
    resume: Mapped[list["ResumesModel"]] = relationship(back_populates="vacancy")