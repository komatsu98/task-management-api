from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.task import Task
from app.schemas.common import PaginationMetadata, SortOrder
from app.schemas.task import TaskCreate, TaskSortBy, TaskUpdate


def create_task(db: Session, task: TaskCreate, creator_id: int):
    db_task = Task(**task.model_dump(), creator_id=creator_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def filter_tasks(
    db: Session,
    status: Optional[str] = None,
    assignee_id: Optional[int] = None,
    sort_by: Optional[TaskSortBy] = None,
    sort_order: Optional[SortOrder] = None,
    user_id: Optional[int] = None,
    is_employee: bool = False,
    page: int = 0,
    limit: int = 0,
):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)
    if is_employee:
        query = query.filter(Task.assignee_id == user_id)

    # Get total items count
    total_items = query.count()

    # Apply sorting
    if sort_by == TaskSortBy.created_at:
        query = query.order_by(
            Task.created_at.asc()
            if sort_order == SortOrder.asc
            else Task.created_at.desc()
        )
    elif sort_by == TaskSortBy.due_date:
        query = query.order_by(
            Task.due_date.asc()
            if sort_order == SortOrder.asc
            else Task.due_date.desc()
        )
    elif sort_by == TaskSortBy.status:
        query = query.order_by(
            Task.status.asc()
            if sort_order == SortOrder.asc
            else Task.status.desc()
        )

    # Apply pagination
    items_per_page = limit
    total_pages = (total_items + limit - 1) // limit
    tasks = query.offset((page - 1) * limit).limit(limit).all()

    metadata = PaginationMetadata(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items_per_page=items_per_page,
    )

    return tasks, metadata


def get_task(
    db: Session,
    task_id: int,
    user_id: Optional[int] = None,
    is_employee: bool = False,
):
    query = db.query(Task).filter(Task.id == task_id)
    if is_employee:
        query = query.filter(Task.assignee_id == user_id)
    return query.first()


def update_task(
    db: Session,
    task_id: int,
    task_update: TaskUpdate,
    user_id: int,
    is_employee: bool,
):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise Exception("Task not found")
    if is_employee and db_task.assignee_id != user_id:
        raise Exception("Not authorized")

    db_task.status = task_update.status
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, user_id: int, is_employee: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise Exception("Task not found")
    if is_employee and db_task.assignee_id != user_id:
        raise Exception("Not authorized")

    db.delete(db_task)
    db.commit()
    return True
