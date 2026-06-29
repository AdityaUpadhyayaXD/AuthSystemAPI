from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import hash_password
from app.schemas.auth import LoginRequest
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.services.token_service import TokenService

class AuthService:
    @staticmethod
    def login(
        db: Session,
        request: LoginRequest
    ):

        user = db.query(User).filter(
            User.username == request.username
        ).first()

        if not user:
            return None, "Invalid username or password"

        if not verify_password(
            request.password,
            user.password_hash
        ):
            return None, "Invalid username or password"

        access_token = create_access_token(
            user.username
        )

        refresh_token = TokenService.create(
            db,
            user
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }, None