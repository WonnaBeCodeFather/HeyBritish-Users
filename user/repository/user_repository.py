from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.models.users import User


class UserRepository:
    @classmethod
    async def add(cls, session: AsyncSession, data: dict) -> User:
        user_data = {key: value for key, value in data.items() if key in User.__table__.columns.keys()}

        user = User(**user_data)
        session.add(user)
        await session.flush()
        return user

    @classmethod
    async def get(cls, session: AsyncSession, pk: int) -> User | None:
        user = await session.get(User, pk)
        return user

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> User | None:
        req = select(User).filter(email == User.email)
        user = await session.execute(req)
        return user.scalars().one()

    @classmethod
    async def change_password(cls, session: AsyncSession, password: str, pk: int) -> User:
        user = await cls.get(session=session, pk=pk)
        user.password = password
        await session.flush()
        return user

    @classmethod
    async def update(cls, session: AsyncSession, data: dict, pk: int) -> User:
        user: User = await cls.get(session=session, pk=pk)
        for key, value in data.items():
            setattr(user, key, value)
        await session.flush()
        await session.refresh(user)
        return user
