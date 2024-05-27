from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import TutorStudent


class TutorStudentRepository:
    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> TutorStudent:
        instance = TutorStudent(**data)
        session.add(instance)
        await session.flush()
        return instance

