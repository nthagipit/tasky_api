from datetime import datetime
from app.core.exception import AppException
from app.core.logging import logging
from app.models import Task
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.base_schema import DataResponse
from app.schemas.task_schema import TaskCreateSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import timezone

logger = logging.getLogger("app.services.task_service")


def get_task_today_by_user_id(user: User, db: Session):
    data =  db.query(Task).filter(
        Task.user_id == user.id, 
        func.date(Task.created_at) == datetime.now(timezone.utc).date()
        ).first()

    return DataResponse.custom_response("200", data=data, message="Tasks retrieved successfully")

def create_task_for_user(user: User, data: TaskCreateSchema, db: Session):
    new_task = Task(
        title=data.title,
        description=data.description,
        user_id=user.id
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"User {user.id} already has a task for today: {e}")
        raise AppException(status_code=409, message="You already have a task for today.")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while creating task: {e}")
        raise AppException(status_code=500, message="Failed to create task")
    
    return DataResponse.custom_response("201", data=new_task, message="Task created successfully")

def get_task_by_id(task_id: str, db: Session):
    task = check_task_exists(task_id, db)
    return DataResponse.custom_response("200", data=task, message="Task retrieved successfully")

def update_task_for_user(task_id: str, data: TaskCreateSchema, db: Session):
    task = check_task_exists(task_id, db)
    task.title = data.title
    task.description = data.description
    task.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(task)
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while updating task: {e}")
        raise AppException(status_code=500, message="Failed to update task")

    return DataResponse.custom_response("200", data=task, message="Task updated successfully")

def delete_task_for_user(task_id: str, db: Session):
    task = check_task_exists(task_id, db)

    try:
        db.delete(task)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while deleting task: {e}")
        raise AppException(status_code=500, message="Failed to delete task")

    return DataResponse.custom_response("200", data=None, message="Task deleted successfully")

def check_task_exists(task_id: str, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise AppException(status_code=404, message="Task not found")
    
    return task