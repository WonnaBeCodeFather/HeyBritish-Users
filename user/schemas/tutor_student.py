import datetime

from pydantic import BaseModel


class TutorStudentCreateSchema(BaseModel):
    student_id: int
    tutor_id: int

    class Config:
        from_attributes = True


class TutorStudentUpdateSchema(TutorStudentCreateSchema):
    pass


class TutorStudentSchema(TutorStudentCreateSchema):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime