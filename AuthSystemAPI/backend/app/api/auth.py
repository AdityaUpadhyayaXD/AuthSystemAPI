from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from fastapi import Response
from app.schemas.auth import LoginRequest



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

    response.set_cookie(
        key="access_token",
        value=data["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 30
    )

    response.set_cookie(
        key="refresh_token",
        value=data["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30
    )

    return {
        "message": "Login successful",
        "username": data["user"].username
    }