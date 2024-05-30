from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenPayload(BaseModel):
    sub: str
    exp: float


class Token(BaseModel):
    access_token: str
    token_type: str
