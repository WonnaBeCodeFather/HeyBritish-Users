from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import Student, User, TutorStudent, Tutor


class StudentRepository:
    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> Student:
        student = Student(**data)
        session.add(student)
        await session.flush()
        return student

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> Student | None:
        student = await session.get(Student, pk)
        return student

    @classmethod
    async def get_tutors(cls, session: AsyncSession, pk: int) -> list:
        stmt = (
            select(User.first_name, User.last_name, User.email, User.id, User.created_at, User.updated_at,
                   User.phone_number).join(Tutor).join(TutorStudent).filter(
                and_(pk == TutorStudent.student_id, User.status == User.Status.ACTIVE)
                )
        )
        result = await session.execute(stmt)

        return [r._mapping for r in result]
    # @classmethod
    # async def get_students

    async def delete(self):
        pass

    async def update(self):
        pass