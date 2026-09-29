from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class TaskDetail(BaseModel):
    __tablename__ = 'task_details'

    task_id: Mapped[str] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    task: Mapped['Task'] = relationship(back_populates='items')