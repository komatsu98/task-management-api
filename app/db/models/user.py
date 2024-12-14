from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRoleEnum(str, PyEnum):
    employee = "employee"
    employer = "employer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRoleEnum), nullable=False)

    # Relationships
    assigned_tasks = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assignee_id"
    )
    created_tasks = relationship(
        "Task", back_populates="creator", foreign_keys="Task.creator_id"
    )
