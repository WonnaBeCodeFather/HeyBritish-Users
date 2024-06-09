import datetime
from pydantic import BaseModel


class TutorCreateSchema(BaseModel):
    user_id: int
    rate: float
    cost_per_lesson: float

    class ConfigDict:
        from_attributes = True


class TutorUpdateSchema(TutorCreateSchema):
    pass


class TutorSchema(TutorCreateSchema):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetTutorStudentsSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    first_name: str
    last_name: str
    email: str
    cost: float
    phone_number: str
