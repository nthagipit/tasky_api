from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskDetailSchema(BaseModel):
    id: str
    content: str
    checked: bool
    position: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskDetailCreateSchema(BaseModel):
    content: str
    position: int | None = None


class TaskDetailUpdateSchema(BaseModel):
    content: str | None = None
    checked: bool | None = None
    position: int | None = None
