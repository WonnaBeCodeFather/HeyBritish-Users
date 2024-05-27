from fastapi import APIRouter
from user.db import session
from user.schemas.student import StudentCreateSchema, StudentSchema, GetStudentTutorSchema
from user.schemas.tutor import TutorCreateSchema, TutorSchema, GetTutorStudentsSchema
from user.schemas.tutor_student import TutorStudentCreateSchema
from user.schemas.user import UserCreateSchema, UserSchema
from user.services.student_service import StudentService
from user.services.tutor_service import TutorService
from user.services.tutor_student_service import TutorUserService
from user.services.user_service import UserService
from user.utils import rollback_on_exception

router = APIRouter(prefix="/user", tags=["users"])


@router.post('/create', response_model=UserSchema)
@rollback_on_exception
async def create_user(db_session: session, data: UserCreateSchema):
    return await UserService.add(session=db_session, data=data)


@router.post('/create-tutor', response_model=TutorSchema)
@rollback_on_exception
async def create_tutor(db_session: session, data: TutorCreateSchema):
    return await TutorService.add(session=db_session, data=data)


@router.post('/create-student', response_model=StudentSchema)
@rollback_on_exception
async def create_tutor(db_session: session, data: StudentCreateSchema):
    return await StudentService.add(session=db_session, data=data)


@router.get('/{pk}', response_model=UserSchema)
async def get_user(pk: int, db_session: session):
    return await UserService.get(session=db_session, pk=pk)


@router.post('/bind-student-to-the-tutor')
@rollback_on_exception
async def bind_student_to_the_tutor(db_session: session, data: TutorStudentCreateSchema):
    return await TutorUserService.add(session=db_session, data=data)


@router.get('/tutor/{pk}/get-students', response_model=list[GetTutorStudentsSchema])
async def get_students_by_tutor(pk: int, db_session: session):
    return await TutorService.get_tutor_students(pk=pk, session=db_session)


@router.get('/student/{pk}/get-tutors', response_model=list[GetStudentTutorSchema])
async def get_students_by_tutor(pk: int, db_session: session):
    return await StudentService.get_student_tutors(pk=pk, session=db_session)
