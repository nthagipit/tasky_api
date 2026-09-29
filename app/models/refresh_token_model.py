import uuid
from datetime import datetime, timezone
from sqlalchemy import  String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship,Mapped, mapped_column
from app.models.base_model import BaseModel

class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    user_id : Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash : Mapped[str] = mapped_column(String, nullable=False, index=True)
    expires_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked : Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")

