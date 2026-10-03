from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.schemas.task_detail_schema import TaskDetailSchema

class TaskSchema(BaseModel):
    id: str
    title: str
    description: str | None = None
    checked: bool
    updated_at: datetime
    created_at: datetime
    items: list[TaskDetailSchema] =  Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None
