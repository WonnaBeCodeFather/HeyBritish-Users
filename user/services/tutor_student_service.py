from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import TutorStudent
from user.repository.tutor_student_repository import TutorStudentRepository
from user.schemas.tutor_student import TutorStudentCreateSchema, TutorStudentSchema


class TutorUserService:

    @classmethod
    async def add(cls, session: AsyncSession, data: TutorStudentCreateSchema) -> TutorStudentSchema:
        try:
            instance: TutorStudent = await TutorStudentRepository.add(session=session, data=data.dict())
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return TutorStudentSchema.from_orm(instance)


