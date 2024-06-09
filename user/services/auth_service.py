import os
from typing import Union, Any

from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from passlib.context import CryptContext
import datetime

from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from user.db import get_db_session
from user.models.users import User
from user.repository.user_repository import UserRepository
from user.schemas.auth import TokenSchema, TokenPayload
from user.schemas.user import DBUserSchema

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="user/login",
    scheme_name="JWT"
)


class AuthService:
    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return password_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_pass: str) -> bool:
        verified = password_context.verify(password, hashed_pass)
        if not verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
        return verified

    @classmethod
    def __create_token(cls, subject: Union[str, Any], expire_minutes: int, is_access_token: bool = True) -> str:
        expires_delta = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=expire_minutes)
        expires_delta.timestamp()
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY if is_access_token else JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    @classmethod
    async def login(cls, db_session: AsyncSession, email: str, password: str) -> TokenSchema:
        try:
            user: User = await UserRepository.get_by_email(session=db_session, email=email)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
        AuthService.verify_password(password=password, hashed_pass=user.password)
        access_token = AuthService.__create_token(subject=user.email,
                                                  expire_minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        refresh_token = AuthService.__create_token(subject=user.email,
                                                   expire_minutes=int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')),
                                                   is_access_token=False)
        return TokenSchema(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    async def get_current_user(cls, token: str = Depends(reuseable_oauth),
                               db_session: AsyncSession = Depends(get_db_session)) -> DBUserSchema:
        token_data = cls.__check_token(token=token)

        user: User = await UserRepository.get_by_email(session=db_session, email=token_data.sub)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return DBUserSchema.model_validate(user)

    @classmethod
    def __check_token(cls, token, is_access_token: bool = True) -> TokenPayload:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY if is_access_token else JWT_REFRESH_SECRET_KEY,
                                 algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"})
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data

    @classmethod
    async def refresh_tokens(cls, refresh_token: str, db_session: AsyncSession) -> TokenSchema:
        token_data = cls.__check_token(token=refresh_token, is_access_token=False)

        user: User = await UserRepository.get_by_email(session=db_session, email=token_data.sub)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        access_token: str = cls.__create_token(subject=user.email, expire_minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token: str = cls.__create_token(subject=user.email, expire_minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))

        return TokenSchema(access_token=access_token, refresh_token=refresh_token)
