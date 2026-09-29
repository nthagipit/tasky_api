from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.task_model import Task


class User(BaseModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default='USER', nullable=False)

    tasks: Mapped[list['Task']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")