# File: services/auth_service.py
# Authentication business logic: user login (credential verification)
# and registration (account creation with duplicate-email check).
# Called by the auth route handlers and depends on core/security.py.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.services.activity_service import log_activity


# Validates email + password against the database, issues a JWT on success.
# Called by POST /auth/login. Returns (token, user) or raises ValueError.
def authenticate_user(db: Session, *, email: str, password: str) -> tuple[str, User]:
    # Look up the user by email — fail early if not found.
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        raise ValueError("Invalid credentials")

    # Verify the password hash against the stored hash.
    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    token = create_access_token(subject=str(user.id), role=user.role.name)
    log_activity(db, user_id=user.id, action="login", entity_type="user", entity_id=str(user.id), details={"email": user.email})
    return token, user


# Creates a new user account with role "user", issues a JWT on success.
# Called by POST /auth/register. Raises ValueError if email is taken.
def register_user(db: Session, *, name: str, email: str, password: str) -> tuple[str, User]:
    # Duplicate-email check — emails must be unique.
    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None:
        raise ValueError("Email already registered")

    # Fetch the default "user" role (created during bootstrap seeding).
    user_role = db.scalar(select(Role).where(Role.name == "user"))
    if user_role is None:
        raise ValueError("Default user role not found")

    # Hash the password and persist the new user.
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
