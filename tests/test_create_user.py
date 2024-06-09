import pytest
from httpx import AsyncClient

from tests.conftest import async_session_maker
from user.models.users import Tenant, User, Student, Tutor
from sqlalchemy import select


@pytest.fixture(scope="module")
async def create_tenant() -> None:
    async with async_session_maker() as session:
        tenant = Tenant(name='test')
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)


@pytest.mark.usefixtures("create_tenant")
class TestUser:
    @classmethod
    async def test_create_student(cls, ac: AsyncClient):
        data = {
            "first_name": "string",
            "last_name": "string",
            "phone_number": "string",
            "email": "Student_john_doe@example.com",
            "tenant_id": 1,
            "status": "active",
            "role": "student",
            "password": "string"
        }

        response = await ac.post("/user/create", json=data)
        assert response.status_code == 201
        response_json = response.json()
        assert response_json["first_name"] == data["first_name"]
        assert response_json["last_name"] == data["last_name"]
        assert response_json["email"] == data["email"].lower()
        async with async_session_maker() as session:
            user_query = select(User).where(response_json["email"] == User.email)
            user_result = await session.execute(user_query)
            user = user_result.scalar()

            student_query = select(Student).where(user.id == Student.user_id)
            student_result = await session.execute(student_query)
            student = student_result.scalars().one_or_none()

        assert student
        assert student.user_id == user.id

    @classmethod
    async def test_create_tutor(cls, ac: AsyncClient):
        data = {
            "first_name": "string",
            "last_name": "string",
            "phone_number": "string",
            "email": "tutor_john_doe@example.com",
            "tenant_id": 1,
            "status": "active",
            "role": "tutor",
            "cost_per_lesson": 12,
            "rate": 10,
            "password": "string"
        }

        response = await ac.post("/user/create", json=data)
        assert response.status_code == 201
        response_json = response.json()
        assert response_json["email"] == data["email"]
        assert response_json["first_name"] == data["first_name"]
        assert response_json["last_name"] == data["last_name"]
        async with async_session_maker() as session:
            user_query = select(User).where(response_json["email"] == User.email)
            user_result = await session.execute(user_query)
            user = user_result.scalar()

            tutor_query = select(Tutor).where(user.id == Tutor.user_id)
            tutor_result = await session.execute(tutor_query)
            tutor = tutor_result.scalars().one_or_none()

        assert user.email == data["email"]
        assert tutor
        assert tutor.user_id == user.id
        assert tutor.cost_per_lesson == data["cost_per_lesson"]
        assert tutor.rate == data["rate"]

    @classmethod
    async def test_create_user_with_existing_email(cls, ac: AsyncClient):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "631564378",
            "email": "student_john_doe@example.com",
            "tenant_id": 1,
            "status": "active",
            "role": "tutor",
            "cost_per_lesson": 50.0,
            "rate": 4.5,
            "password": "securepassword"
        }

        response = await ac.post("user/create", json=data)
        assert response.status_code == 400
        assert response.json()["detail"] == "email already exists"

    @classmethod
    async def test_create_user_with_invalid_tenant_id(cls, ac: AsyncClient):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "phone_number": "631564378",
            "email": "jane.doe@example.com",
            "tenant_id": 999,
            "status": "active",
            "role": "student",
            "password": "securepassword"
        }

        response = await ac.post("user/create", json=data)
        assert response.status_code == 400
        assert response.json()["detail"] == "tenant_id doesn't exist"
        async with async_session_maker() as session:
            query = select(User).where(data["email"] == User.email)
            result = await session.execute(query)
            result = result.scalars().all()
        assert len(result) == 0
