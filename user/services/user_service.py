from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import User
from user.repository.user_repository import UserRepository
from user.schemas.student import StudentCreateSchema
from user.schemas.tutor import TutorCreateSchema
from user.schemas.user import UserCreateSchema, UserSchema, RoleEnum
from user.services.student_service import StudentService
from user.services.tutor_service import TutorService


class UserService:

    @classmethod
    async def add(cls, session: AsyncSession, data: UserCreateSchema) -> UserSchema:
        try:
            user: User = await UserRepository.add(session=session, data=data.dict())
            if data.role == RoleEnum.tutor:
                await TutorService.add(session=session, data=TutorCreateSchema(user_id=user.id,
                                                                               cost_per_lesson=data.cost_per_lesson,
                                                                               rate=data.rate))
            else:
                await StudentService.add(session=session, data=StudentCreateSchema(user_id=user.id))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exist")
        return UserSchema.from_orm(user)

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> UserSchema:
        user: User = await UserRepository.get(session=session, pk=pk)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserSchema.from_orm(user)

    @classmethod
    async def get_list(cls):
        pass
