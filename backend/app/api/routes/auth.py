# File: api/routes/auth.py
# Authentication route handlers: login, register, and current-user profile.
# All three endpoints are public (no auth required for login/register),
# while /me uses JWT-based dependency injection for identity resolution.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserRead
from app.services.auth_service import authenticate_user, register_user

router = APIRouter()



# POST /auth/login — validates credentials and returns a JWT access token.
@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        token, _user = authenticate_user(db, email=payload.email, password=payload.password)
        return TokenResponse(access_token=token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from None


# POST /auth/register — creates a new "user"-role account and returns a JWT.
@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        token, _user = register_user(db, name=payload.name, email=payload.email, password=payload.password)
        return TokenResponse(access_token=token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None


# GET /auth/me — returns the authenticated user's profile (JWT-protected).
@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)) -> UserRead:
    return current_user
