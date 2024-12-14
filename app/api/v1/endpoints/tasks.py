from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.common import SortOrder
from app.schemas.task import (
    TaskCreate,
    TaskPaginatedResponse,
    TaskResponse,
    TaskSortBy,
    TaskUpdate,
)
from app.services.auth_service import check_user_role
from app.services.task_service import (
    create_task,
    delete_task,
    filter_tasks,
    get_task,
    update_task,
)

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task_handler(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_user_role(current_user, "employer")
    return create_task(db, task, current_user.id)


@router.get("/tasks", response_model=TaskPaginatedResponse)
def filter_tasks_handler(
    status: Optional[str] = None,
    assignee_id: Optional[int] = None,
    sort_by: TaskSortBy = Query(TaskSortBy.created_at),
    sort_order: SortOrder = Query(SortOrder.asc),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_employee = current_user.role == "employee"
    tasks, metadata = filter_tasks(
        db=db,
        status=status,
        assignee_id=assignee_id,
        sort_by=sort_by,
        sort_order=sort_order,
        user_id=current_user.id,
        is_employee=is_employee,
        page=page,
        limit=limit,
    )
    return TaskPaginatedResponse(
        data=tasks,
        metadata=metadata,
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_handler(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_employee = current_user.role == "employee"
    task = get_task(
        db, task_id, user_id=current_user.id, is_employee=is_employee
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_handler(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_employee = current_user.role == "employee"
    updated_task = update_task(
        db, task_id, task_update, current_user.id, is_employee
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task_handler(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_employee = current_user.role == "employee"
    delete_task(db, task_id, current_user.id, is_employee)
    return {}
