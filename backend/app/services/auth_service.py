from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.services.activity_service import log_activity


def authenticate_user(db: Session, *, email: str, password: str) -> tuple[str, User]:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    token = create_access_token(subject=str(user.id), role=user.role.name)
    log_activity(db, user_id=user.id, action="login", entity_type="user", entity_id=str(user.id), details={"email": user.email})
    return token, user


def register_user(db: Session, *, name: str, email: str, password: str) -> tuple[str, User]:
    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None:
        raise ValueError("Email already registered")

    user_role = db.scalar(select(Role).where(Role.name == "user"))
    if user_role is None:
        raise ValueError("Default user role not found")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role_id=user_role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id), role=user.role.name)
    log_activity(db, user_id=user.id, action="register", entity_type="user", entity_id=str(user.id), details={"email": user.email})
    return token, user
