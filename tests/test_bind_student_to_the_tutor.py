import pytest
from httpx import AsyncClient

from tests.conftest import async_session_maker
from user.models.users import Tenant, User, Student, Tutor, TutorStudent
from sqlalchemy import select


@pytest.fixture(scope="module")
async def create_tenant() -> None:
    async with async_session_maker() as session:
        tenant = Tenant(name='test')
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)


@pytest.fixture(scope="module")
async def create_student() -> None:
    async with async_session_maker() as session:
        data = {
            "first_name": "string",
            "last_name": "string",
            "phone_number": "string",
            "email": "student_john_doe@example.com",
            "tenant_id": 1,
            "status": "active",
            "password": "string"
        }
        user = User(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        student = Student(user_id=user.id)
        session.add(student)
        await session.commit()
        await session.refresh(student)


@pytest.fixture(scope="module")
async def create_tutor() -> None:
    async with async_session_maker() as session:
        data = {
            "first_name": "string",
            "last_name": "string",
            "phone_number": "string",
            "email": "tutor_john_doe@example.com",
            "tenant_id": 1,
            "status": "active",
            "password": "string",
        }
        user = User(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        tutor = Tutor(user_id=user.id, cost_per_lesson=12, rate=10)
        session.add(tutor)
        await session.commit()
        await session.refresh(tutor)


@pytest.mark.usefixtures("create_tenant", "create_student", "create_tutor")
class TestBindStudentToTheTutor:
    @staticmethod
    async def get_student() -> Student:
        async with async_session_maker() as session:
            student_query = select(Student)
            student_result = await session.execute(student_query)
            return student_result.scalar()

    @staticmethod
    async def get_tutor() -> Tutor:
        async with async_session_maker() as session:
            tutor_query = select(Tutor)
            tutor_result = await session.execute(tutor_query)
            return tutor_result.scalar()

    @classmethod
    async def test_bind_student_to_the_tutor(cls, ac: AsyncClient):
        student = await cls.get_student()
        tutor = await cls.get_tutor()
        assert student
        assert tutor
        response = await ac.post("user/bind-student-to-the-tutor",
                                 json={"student_id": student.id, "tutor_id": tutor.id})
        assert response.status_code == 201
        async with async_session_maker() as session:
            student_tutor_query = select(TutorStudent)
            student_tutor_result = await session.execute(student_tutor_query)
            student_tutor = student_tutor_result.scalars().all()
        assert len(student_tutor) == 1
        assert student_tutor[0].student_id == student.id
        assert student_tutor[0].tutor_id == tutor.id

    @classmethod
    async def test_bind_student_to_the_tutor_with_wrong_student(cls, ac: AsyncClient):
        tutor = await cls.get_tutor()
        response = await ac.post("user/bind-student-to-the-tutor", json={"student_id": 1212, "tutor_id": tutor.id})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    @classmethod
    async def test_bind_student_to_the_tutor_with_wrong_tutor(cls, ac: AsyncClient):
        student = await cls.get_student()
        response = await ac.post("user/bind-student-to-the-tutor",
                                 json={"student_id": student.id, "tutor_id": 123123123})
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
