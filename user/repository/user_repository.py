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

    async def delete(self):
        pass

    async def update(self):
        pass
