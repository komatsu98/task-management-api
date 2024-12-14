from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class TaskStatusEnum(str, PyEnum):
    pending = "pending"
    inprogress = "inprogress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        Enum(TaskStatusEnum), default=TaskStatusEnum.pending, nullable=False
    )
    created_at = Column(
        DateTime, default=datetime.now(tz=timezone.utc), nullable=False
    )
    due_date = Column(DateTime, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )
    creator = relationship(
        "User", back_populates="created_tasks", foreign_keys=[creator_id]
    )
