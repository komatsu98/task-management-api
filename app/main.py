from fastapi import FastAPI

from app.api.v1.endpoints import auth, task_summary, tasks
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

# Include routers
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(
    task_summary.router, prefix="/api/v1", tags=["tasks summary"]
)
