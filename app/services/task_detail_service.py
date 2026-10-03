from datetime import datetime
from app.core.logging import logging
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.exception import AppException
from app.models.task_detail_model import TaskDetail
from app.schemas.base_schema import DataResponse
from app.schemas.task_detail_schema import TaskDetailCreateSchema, TaskDetailUpdateSchema


logger = logging.getLogger("app.services.task_detail_service")

def create_task_detail(task_id: str, data: TaskDetailCreateSchema, db: Session):
    if data.position is not None:
        new_position = data.position
    else:
        max_pos = (
            db.query(func.max(TaskDetail.position))
            .filter(TaskDetail.task_id == task_id)
            .scalar()
        )
        new_position = (max_pos + 1) if max_pos is not None else 0

    task_detail = TaskDetail(
        task_id=task_id,
        content=data.content,
        position=new_position,
        checked=False,
        created_at=datetime.utcnow()
    )

    try:
        db.add(task_detail)
        db.commit()
        db.refresh(task_detail)
        return DataResponse.custom_response("201", data=task_detail, message="Task detail created successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while creating task detail: {e}")
        raise AppException(status_code=500, message="Failed to create task detail")


def update_task_detail(task_detail_id: str, data: TaskDetailUpdateSchema, db: Session):
    task_detail = check_task_detail_exists(task_detail_id, db)
    if data.checked is not None:
        task_detail.checked = data.checked

    if data.content is not None:
        task_detail.content = data.content

    if data.position is not None:
        task_detail.position = data.position

    task_detail.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(task_detail)
        return DataResponse.custom_response("200", data=task_detail, message="Task detail updated successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while updating task detail: {e}")
        raise AppException(status_code=500, message="Failed to update task detail")


def delete_task_detail(task_detail_id: str, db: Session):
    task_detail = check_task_detail_exists(task_detail_id, db)
    try:
        db.delete(task_detail)
        db.commit()

        return DataResponse.custom_response("200", data=None, message="Task detail deleted successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error occurred while deleting task detail: {e}")
        raise AppException(status_code=500, message="Failed to delete task detail")


def check_task_detail_exists(task_detail_id: str, db: Session):
    task_detail = db.query(TaskDetail).filter(TaskDetail.id == task_detail_id).first()
    if not task_detail:
        logger.warning(f"Task detail with ID {task_detail_id} not found")
        raise AppException(status_code=404, message="Task detail not found")
    
    return task_detail