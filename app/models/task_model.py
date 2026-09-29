from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Task(BaseModel):
    __tablename__ = 'tasks'

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped['User'] = relationship(back_populates='tasks')
    items: Mapped[list['TaskDetail']] = relationship(
        back_populates='task',
        cascade='all, delete-orphan',
        passive_deletes=True,
        order_by='TaskDetail.position',
    )