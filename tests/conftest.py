import asyncio
import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from user.db import get_db_session
from user.main import app
from user.models.users import Base

load_dotenv()

DATABASE_URL_TEST = os.environ.get('TEST_DATABASE_URL')
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

client = TestClient(app)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()


app.dependency_overrides[get_db_session] = override_get_async_session


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
