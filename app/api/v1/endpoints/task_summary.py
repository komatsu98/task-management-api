from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task_summary import TaskSummaryPaginatedResponse
from app.services.task_summary_service import get_employee_task_summary

router = APIRouter()


@router.get(
    "/employees/tasks-summary", response_model=TaskSummaryPaginatedResponse
)
async def employee_task_summary_handler(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    summaries, metadata = get_employee_task_summary(db, page, limit)
    return TaskSummaryPaginatedResponse(data=summaries, metadata=metadata)
