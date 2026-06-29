import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server_fastapi.database.models.base import Base


class UserType(enum.Enum):
    USER = 'USER'
    VIP = 'VIP'
    ADMIN = 'ADMIN'


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    pwd_hash: Mapped[str] = mapped_column()
    resume_limit: Mapped[int] = mapped_column(default=100)
    token_hash: Mapped[str] = mapped_column()
    role: Mapped[UserType] = mapped_column(Enum(UserType, name="user_role_enum"), default=UserType.USER)
    deleted: Mapped[bool] = mapped_column(default=False)

    vacancies: Mapped[list["VacanciesModel"]] = relationship(back_populates="user")