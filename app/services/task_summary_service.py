from sqlalchemy.orm import Session

from app.db.models.task import Task, TaskStatusEnum
from app.db.models.user import User, UserRoleEnum
from app.schemas.common import PaginationMetadata
from app.schemas.task_summary import EmployeeTaskSummary


def get_employee_task_summary(db: Session, page: int, limit: int):
    # Get employees with pagination
    employees = (
        db.query(User)
        .filter(User.role == UserRoleEnum.employee)
        .with_entities(User.id, User.username)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    total_employees = (
        db.query(User).filter(User.role == UserRoleEnum.employee).count()
    )

    summaries = []

    for employee in employees:
        total_tasks_assigned = (
            db.query(Task).filter(Task.assignee_id == employee.id).count()
        )

        completed_tasks = (
            db.query(Task)
            .filter(
                Task.assignee_id == employee.id,
                Task.status == TaskStatusEnum.completed,
            )
            .count()
        )

        summaries.append(
            EmployeeTaskSummary(
                employee_id=employee.id,
                username=employee.username,
                total_tasks_assigned=total_tasks_assigned,
                completed_tasks=completed_tasks,
            )
        )

    items_per_page = limit
    total_pages = (total_employees + limit - 1) // limit

    metadata = PaginationMetadata(
        total_items=total_employees,
        total_pages=total_pages,
        current_page=page,
        items_per_page=items_per_page,
    )

    return summaries, metadata
