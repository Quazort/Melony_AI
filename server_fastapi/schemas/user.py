from typing import Annotated

from pydantic import BaseModel, StringConstraints, EmailStr


class UserRegistrationSchema(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
    email: EmailStr


class UserLoginSchema(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
