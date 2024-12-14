from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.models.user import User
from app.db.session import get_db
from app.services.auth_service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

unauthenticated_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    try:
        token_payload = decode_access_token(token)
    except Exception:
        raise unauthenticated_exception

    user = get_user(db, token_payload["sub"])
    if user is None:
        raise unauthenticated_exception

    return user
