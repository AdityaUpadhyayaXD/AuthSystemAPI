from fastapi import APIRouter
from fastapi import Depends

from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }