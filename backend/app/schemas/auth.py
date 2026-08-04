# File: schemas/auth.py
# Pydantic schemas for the authentication domain. Defines request shapes
# for login/register endpoints and response shapes for token exchange
# and user profile retrieval.

from app.schemas.base import ORMBaseModel


# POST /auth/login — validates email + password from the request body.
class LoginRequest(ORMBaseModel):
    email: str
    password: str


# POST /auth/register — validates name + email + password for new accounts.
class RegisterRequest(ORMBaseModel):
    name: str
    email: str
    password: str
class TokenResponse(ORMBaseModel):
    access_token: str
    token_type: str = "bearer"


# Nested schema for the user's role, used inside UserRead.
class RoleRead(ORMBaseModel):
    id: int
    name: str


# GET /auth/me — user profile including their RBAC role.
class UserRead(ORMBaseModel):
    id: int
    name: str
    email: str
    role: RoleRead
