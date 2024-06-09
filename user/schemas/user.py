import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, validator, field_validator

from user.models.users import User


class RoleEnum(str, Enum):
    student = 'student'
    tutor = 'tutor'


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    tenant_id: int
    status: User.Status = User.Status.inactive.value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, email):
        return email.lower()

    class ConfigDict:
        from_attributes = True


class UserCreateSchema(UserBase):
    role: RoleEnum
    cost_per_lesson: float | None = None
    rate: float | None = None
    password: str


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    status: User.Status | None = None

    class ConfigDict:
        from_attributes = True


class UserSchema(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class DBUserSchema(UserSchema):
    password: str


class ChangePasswordRequestSchema(BaseModel):
    current_password: str
    new_password: str
