from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import Student
from user.repository.student_repository import StudentRepository
from user.schemas.student import StudentCreateSchema, StudentSchema, GetStudentTutorSchema


class StudentService:

    @classmethod
    async def add(cls, session: AsyncSession, data: StudentCreateSchema) -> StudentSchema:
        try:
            student: Student = await StudentRepository.add(session=session, data=data.model_dump())
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return StudentSchema.model_validate(student, from_attributes=True)

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> StudentSchema:
        student: Student = await StudentRepository.get(session=session, pk=pk)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return StudentSchema.model_validate(student, from_attributes=True)

    @classmethod
    async def get_student_tutors(cls, session: AsyncSession, pk) -> list[GetStudentTutorSchema]:
        instances = await StudentRepository.get_tutors(session=session, pk=pk)
        return [GetStudentTutorSchema(**instance) for instance in instances]