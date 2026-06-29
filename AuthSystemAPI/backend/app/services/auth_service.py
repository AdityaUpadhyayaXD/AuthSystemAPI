from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth import RegisterRequest, LoginRequest

from app.core.security import (
    hash_password,
    verify_password
)

from app.core.jwt import create_access_token

from app.services.token_service import TokenService


class AuthService:

    @staticmethod
    def register(
        db: Session,
        request: RegisterRequest
    ):

        existing_username = db.query(User).filter(
            User.username == request.username
        ).first()

        if existing_username:
            return None, "Username already exists"

        existing_email = db.query(User).filter(
            User.email == request.email
        ).first()

        if existing_email:
            return None, "Email already exists"

        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(
                request.password
            )
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user, None


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