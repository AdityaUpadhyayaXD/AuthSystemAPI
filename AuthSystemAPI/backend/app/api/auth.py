from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import RegisterRequest

from app.services.auth_service import AuthService

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