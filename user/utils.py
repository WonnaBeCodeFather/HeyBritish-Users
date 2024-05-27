from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


def rollback_on_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: AsyncSession = kwargs.get('db_session')
        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(e) if e else "Internal server error")

    return wrapper
