
from fastapi import Response

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.models.user_model import User
from app.db.base import get_db
from app.schemas.base_schema import DataResponse
from app.services.task_service import create_task_for_user, get_task_today_by_user_id, get_task_by_id, update_task_for_user, delete_task_for_user
from app.middlewares.authenticate import get_current_user
from app.schemas.task_schema import TaskCreateSchema, TaskSchema


router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(get_current_user)])

@router.get("/today", description="Get today's tasks for the authenticated user", response_model=DataResponse[TaskSchema])
async def get_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_task_today_by_user_id(user, db)

@router.post("/today", description="Create a new task for the authenticated user", response_model=DataResponse[TaskSchema], response_model_exclude_none=True)
async def create_task(data: TaskCreateSchema,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_task_for_user(user, data, db)

@router.get("/{task_id}", description="Get a task by ID for the authenticated user", response_model=DataResponse[TaskSchema])
async def get_task(task_id: str,  db: Session = Depends(get_db)):
    return get_task_by_id(task_id, db)

@router.put("/{task_id}", description="Update a task by ID for the authenticated user", response_model=DataResponse[TaskSchema],response_model_exclude_none=True)
async def update_task(task_id: str, data: TaskCreateSchema, db: Session = Depends(get_db)):
    return update_task_for_user(task_id, data, db)

@router.delete("/{task_id}", description="Delete a task by ID for the authenticated user", response_model=DataResponse, response_model_exclude_none=True)
async def delete_task(task_id: str,  db: Session = Depends(get_db)):
    return delete_task_for_user(task_id, db)