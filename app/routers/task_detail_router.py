from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.models.user_model import User
from app.db.base import get_db
from app.schemas.base_schema import DataResponse
from app.schemas.task_detail_schema import TaskDetailSchema, TaskDetailCreateSchema, TaskDetailUpdateSchema
from app.services import task_detail_service
from app.middlewares.authenticate import get_current_user


router = APIRouter(prefix="/task-detail", tags=["task-detail"], dependencies=[Depends(get_current_user)])


@router.post("/{task_id}", description="Create a new task for the authenticated user", response_model=DataResponse[TaskDetailSchema], response_model_exclude_none=True)
async def create_task_detail(task_id: str, data: TaskDetailCreateSchema,  db: Session = Depends(get_db)):
    return task_detail_service.create_task_detail(task_id, data, db)


@router.put("/{task_detail_id}", description="Update a task by ID for the authenticated user", response_model=DataResponse[TaskDetailSchema],response_model_exclude_none=True)
async def update_task_detail(task_detail_id: str, data: TaskDetailUpdateSchema,  db: Session = Depends(get_db), ):
    return task_detail_service.update_task_detail(task_detail_id, data,  db)


@router.delete("/{task_detail_id}", description="Delete a task by ID for the authenticated user", response_model=DataResponse, response_model_exclude_none=True)
async def delete_task_detail(task_detail_id: str, db: Session = Depends(get_db)):
    return task_detail_service.delete_task_detail(task_detail_id, db)