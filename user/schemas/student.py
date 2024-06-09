import datetime
from pydantic import BaseModel


class StudentCreateSchema(BaseModel):
    user_id: int

    class ConfigDict:
        from_attributes = True


class StudentUpdateSchema(StudentCreateSchema):
    pass


class StudentSchema(StudentCreateSchema):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetStudentTutorSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    first_name: str
    last_name: str
    email: str
    phone_number: str
