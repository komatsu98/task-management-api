from typing import List

from pydantic import BaseModel

from .common import PaginatedResponse


class EmployeeTaskSummary(BaseModel):
    employee_id: int
    username: str
    total_tasks_assigned: int
    completed_tasks: int


class TaskSummaryPaginatedResponse(PaginatedResponse):
    data: List[EmployeeTaskSummary]
