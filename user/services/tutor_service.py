from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import Tutor
from user.repository.tutor_repository import TutorRepository
from user.schemas.tutor import TutorCreateSchema, TutorSchema, GetTutorStudentsSchema


class TutorService:

    @classmethod
    async def add(cls, session: AsyncSession, data: TutorCreateSchema) -> TutorSchema:
        try:
            tutor: Tutor = await TutorRepository.add(session=session, data=data.dict())
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return TutorSchema.from_orm(tutor)

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> TutorSchema:
        tutor: Tutor = await TutorRepository.get(session=session, pk=pk)
        if not tutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return TutorSchema.from_orm(tutor)

    @classmethod
    async def get_tutor_students(cls, session: AsyncSession, pk) -> list[GetTutorStudentsSchema]:
        instances = await TutorRepository.get_students(session=session, pk=pk)
        return [GetTutorStudentsSchema(**instance) for instance in instances]
