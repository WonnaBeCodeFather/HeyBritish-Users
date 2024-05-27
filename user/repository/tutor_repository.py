from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.engine.result import Row
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import Tutor, TutorStudent, User, Student


class TutorRepository:
    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> Tutor:
        tutor = Tutor(**data)
        session.add(tutor)
        await session.flush()
        return tutor

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> Tutor | None:
        tutor = await session.get(Tutor, pk)
        return tutor

    @classmethod
    async def get_students(cls, session: AsyncSession, pk: int) -> list:
        stmt = (
            select(User.first_name, User.last_name, User.email, User.id, User.created_at, User.updated_at,
                   User.phone_number, Student.cost).join(Student).join(TutorStudent).filter(
                and_(pk == TutorStudent.tutor_id, User.status == User.Status.ACTIVE)
                )
        )
        result = await session.execute(stmt)

        return [r._mapping for r in result]

    async def delete(self):
        pass

    async def update(self):
        pass
