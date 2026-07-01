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
