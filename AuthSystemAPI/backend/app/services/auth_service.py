from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import hash_password


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