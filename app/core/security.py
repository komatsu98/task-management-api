from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException, status

from app.core.config import settings
from app.db.models.user import User


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    payload = data.copy()
    payload.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        decoded = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_role(user: User, role: str):
    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
