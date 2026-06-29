from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config import settings


def create_access_token(username: str):

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(username: str):

    expire = datetime.now(UTC) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": username,
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except Exception:

        return None