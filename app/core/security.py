
from datetime import timedelta
from app.core.config import settings
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) ->str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: str, role: str, expires_delta: Optional[timedelta] = None):
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: str, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)

    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)