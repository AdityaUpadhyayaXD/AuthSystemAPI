from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from fastapi import Response
from app.schemas.auth import LoginRequest
from app.core.cookies import set_auth_cookies
from app.core.cookies import clear_auth_cookies
from fastapi import Cookie

from app.core.jwt import (
    verify_token,
    create_access_token
)

from app.services.token_service import TokenService
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    user, error = AuthService.register(
        db,
        request
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "User registered successfully"
    }

@router.post("/login")
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    data, error = AuthService.login(
        db,
        request
    )

    if error:
        raise HTTPException(
            status_code=401,
            detail=error
        )

    set_auth_cookies(
        response,
        data["access_token"],
        data["refresh_token"]
    )    

    return {
        "message": "Login successful",
        "username": data["user"].username
    }
@router.post("/refresh")
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    payload = verify_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    db_token = TokenService.get_valid_refresh_token(
        db,
        refresh_token
    )

    if db_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revoked"
        )

    new_access_token = create_access_token(
        payload["sub"]
    )

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 30
    )

    return {
        "message": "Access token refreshed"
    }
@router.post("/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):

    if refresh_token:
        TokenService.revoke(
            db,
            refresh_token
        )

    clear_auth_cookies(response)

    return {
        "message": "Logged out successfully"
    }
