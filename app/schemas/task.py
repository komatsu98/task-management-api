from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .common import PaginatedResponse


class TaskStatus(str, Enum):
    pending = "pending"
    inprogress = "inprogress"
    completed = "completed"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(TaskBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskSortBy(str, Enum):
    created_at = "created_at"
    due_date = "due_date"
    status = "status"


class TaskPaginatedResponse(PaginatedResponse):
    data: List[TaskResponse]
