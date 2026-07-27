# File: services/bootstrap.py
# Startup seeding logic that ensures the database always has the
# two required roles ("admin", "user") and two default user accounts.
# Called once during application startup from main.py.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db import session as db_session
from app.models.role import Role
from app.models.user import User


DEFAULT_ROLES = ("admin", "user")
DEFAULT_USERS = (
    {"name": "Admin User", "email": "admin@gmail.com", "password": "admin123", "role": "admin"},
    {"name": "Standard User", "email": "user@gmail.com", "password": "user123", "role": "user"},
)


# Idempotent seeder — creates roles and users only if they don't already
# exist. Runs on every startup so fresh databases are always operational.
def seed_defaults() -> None:
    db: Session = db_session.SessionLocal()
    try:
        # Seed roles if missing (e.g. first startup after DB creation).
        roles = {role.name: role for role in db.scalars(select(Role)).all()}
        for role_name in DEFAULT_ROLES:
            if role_name not in roles:
                role = Role(name=role_name)
                db.add(role)
                db.flush()
                roles[role_name] = role
        db.commit()

        # Seed default user accounts if they don't exist yet.
        existing_emails = {user.email for user in db.scalars(select(User)).all()}
        for seed_user in DEFAULT_USERS:
            if seed_user["email"] in existing_emails:
                continue
            db.add(
                User(
                    name=seed_user["name"],
                    email=seed_user["email"],
                    hashed_password=hash_password(seed_user["password"]),
                    role_id=roles[seed_user["role"]].id,
                )
            )
        db.commit()
    finally:
        db.close()
