import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr

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
    status: User.Status = User.Status.INACTIVE

    class Config:
        from_attributes = True


class UserCreateSchema(UserBase):
    role: RoleEnum
    cost_per_lesson: float | None = None
    rate: float | None = None
    password: str


class UserUpdateSchema(UserBase):
    pass


class UserSchema(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
