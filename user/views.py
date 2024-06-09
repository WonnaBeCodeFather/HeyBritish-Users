from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from user.db import session
from user.schemas.auth import TokenSchema
from user.schemas.student import StudentCreateSchema, StudentSchema, GetStudentTutorSchema
from user.schemas.tutor import TutorCreateSchema, TutorSchema, GetTutorStudentsSchema
from user.schemas.tutor_student import TutorStudentCreateSchema, TutorStudentSchema
from user.schemas.user import UserCreateSchema, UserSchema, DBUserSchema, ChangePasswordRequestSchema, UserUpdateSchema
from user.services.auth_service import AuthService
from user.services.student_service import StudentService
from user.services.tutor_service import TutorService
from user.services.tutor_student_service import TutorUserService
from user.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["users"])


@router.post('/create', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(db_session: session, data: UserCreateSchema):
    return await UserService.add(session=db_session, data=data)


@router.post('/create-tutor', response_model=TutorSchema, status_code=status.HTTP_201_CREATED)
async def create_tutor(db_session: session, data: TutorCreateSchema):
    return await TutorService.add(session=db_session, data=data)


@router.post('/create-student', response_model=StudentSchema, status_code=status.HTTP_201_CREATED)
async def create_student(db_session: session, data: StudentCreateSchema):
    return await StudentService.add(session=db_session, data=data)


@router.get('/{pk}', response_model=UserSchema)
async def get_user(pk: int, db_session: session):
    return await UserService.get(session=db_session, pk=pk)


@router.post('/bind-student-to-the-tutor', response_model=TutorStudentSchema, status_code=status.HTTP_201_CREATED)
async def bind_student_to_the_tutor(db_session: session, data: TutorStudentCreateSchema):
    return await TutorUserService.add(session=db_session, data=data)


@router.get('/tutor/{pk}/get-students', response_model=list[GetTutorStudentsSchema])
async def get_students_by_tutor(pk: int, db_session: session):
    return await TutorService.get_tutor_students(pk=pk, session=db_session)


@router.get('/student/{pk}/get-tutors', response_model=list[GetStudentTutorSchema])
async def get_tutors_by_student(pk: int, db_session: session):
    return await StudentService.get_student_tutors(pk=pk, session=db_session)


@router.post('/login', response_model=TokenSchema)
async def login(db_session: session, data: OAuth2PasswordRequestForm = Depends()):
    return await AuthService.login(db_session=db_session, email=data.username, password=data.password)


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[DBUserSchema, Depends(AuthService.get_current_user)],
):
    return current_user


@router.post('/refresh', summary="Refresh access and refresh tokens", response_model=TokenSchema)
async def refresh_tokens(refresh_token: str, db_session: session):
    return await AuthService.refresh_tokens(refresh_token=refresh_token, db_session=db_session)


@router.post('/change_password', response_model=UserSchema)
async def change_password(db_session: session, data: ChangePasswordRequestSchema,
                          current_user: Annotated[DBUserSchema, Depends(AuthService.get_current_user)]):
    return await UserService.change_password(user=current_user, current_password=data.current_password,
                                             new_password=data.new_password, session=db_session)


@router.post('/update', response_model=UserSchema)
async def update_user(db_session: session, data: UserUpdateSchema,
                      current_user: Annotated[DBUserSchema, Depends(AuthService.get_current_user)]):
    return await UserService.update_user(user=current_user, session=db_session, data=data)
