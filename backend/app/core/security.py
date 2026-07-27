# File: core/security.py
# Security primitives for the application: password hashing and verification
# via passlib, and JWT token creation for authenticated sessions.
# Consumed by the auth service and API dependency layer.

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


from app.core.config import settings

# passlib context configured with PBKDF2-SHA256 for secure password storage.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Hashes a plain-text password before storing it in the database.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Compares a plain-text password against a stored hash during login.
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# Creates a signed JWT containing the user ID (sub) and role, with an
# expiration time defined in settings. Called after successful login/registration.
def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
