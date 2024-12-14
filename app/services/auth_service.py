from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password, verify_role
from app.db.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    existing_user = (
        db.query(User).filter(User.username == user.username).first()
    )
    if existing_user:
        raise ValueError("Username already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username, hashed_password=hashed_password, role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def check_user_role(user: User, role: str):
    verify_role(user, role)
