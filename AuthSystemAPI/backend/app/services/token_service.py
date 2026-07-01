from app import database
from app import database
from datetime import datetime, timedelta, UTC

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.user import User

from app.core.config import settings
from app.core.jwt import create_refresh_token


class TokenService:

    @staticmethod
    def create(db: Session, user: User):

        token = create_refresh_token(
            user.username
        )

        refresh = RefreshToken(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(UTC) + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        db.add(refresh)
        db.commit()

        return token
    

    @staticmethod
    def get_valid_refresh_token(
        db: Session,
        token: str
    ):

        return db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.revoked == False
        ).first()
    
    @staticmethod
    def revoke(db: Session, token: str):

        refresh = db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()
    

    @staticmethod
    def revoke(db: Session, token: str):

        refresh = db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()

        if refresh:
            refresh.revoked = True
            db.commit()