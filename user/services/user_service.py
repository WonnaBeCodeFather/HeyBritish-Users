import re

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import User
from user.repository.user_repository import UserRepository
from user.schemas.student import StudentCreateSchema
from user.schemas.tutor import TutorCreateSchema
from user.schemas.user import UserCreateSchema, UserSchema, RoleEnum
from user.services.auth_service import AuthService
from user.services.student_service import StudentService
from user.services.tutor_service import TutorService

load_dotenv()


class UserService:
    @classmethod
    def hash_password_in_payload(cls, payload: UserCreateSchema):
        password = payload.password
        payload.password = AuthService.get_hashed_password(password)
        return payload

    @classmethod
    async def add(cls, session: AsyncSession, data: UserCreateSchema) -> UserSchema:
        try:
            user: User = await UserRepository.add(session=session,
                                                  data=cls.hash_password_in_payload(payload=data).dict())
        except IntegrityError as e:
            error_message = str(e.orig)

            if "email" in error_message and re.search(r"unique constraint", error_message):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")

            if "tenant_id" in error_message and re.search(r"foreign key constraint", error_message):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tenant_id doesn't exist")

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error occurred")

        if data.role == RoleEnum.tutor:
            await TutorService.add(session=session, data=TutorCreateSchema(user_id=user.id,
                                                                           cost_per_lesson=data.cost_per_lesson,
                                                                           rate=data.rate))
        else:
            await StudentService.add(session=session, data=StudentCreateSchema(user_id=user.id))

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
