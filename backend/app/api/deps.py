# File: api/deps.py
# FastAPI dependency-injection module that provides shared dependencies
# for route handlers: database sessions, JWT-authenticated current user,
# and role-based access control (RBAC). Used by every protected endpoint.

from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db import session as db_session
from app.models.user import User

# Bearer-token extraction helper used by FastAPI's dependency injection system.
security_scheme = HTTPBearer(auto_error=False)


# Provides a new SQLAlchemy session per request and ensures it is closed
# after the response is sent. Every route that needs DB access depends on this.
def get_db() -> Generator[Session, None, None]:
    db = db_session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authenticates the caller by decoding the JWT from the Authorization header,
# then loads the corresponding User (including their role) from the database.
# Called on every protected endpoint to establish the request identity.
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Reject requests that do not carry a bearer token.
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    # JWT validation — decodes the token and extracts the user ID (sub claim).
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from None

    # Look up the user by ID and eagerly load their role for RBAC checks.
    user = db.scalar(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == user_id)
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# RBAC guard — returns a dependency that verifies the current user's role
# against the set of allowed roles. Used as: Depends(require_role("admin"))
def require_role(*allowed_roles: str):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.name not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return current_user

    return dependency
