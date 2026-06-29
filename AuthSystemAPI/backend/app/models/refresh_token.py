from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    token = Column(
        String(500),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    revoked = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )