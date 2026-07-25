from app.schemas.base import ORMBaseModel


class LoginRequest(ORMBaseModel):
    email: str
    password: str


class RegisterRequest(ORMBaseModel):
    name: str
    email: str
    password: str


class TokenResponse(ORMBaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleRead(ORMBaseModel):
    id: int
    name: str


class UserRead(ORMBaseModel):
    id: int
    name: str
    email: str
    role: RoleRead
