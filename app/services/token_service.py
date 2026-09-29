from app.core.security import create_access_token, create_refresh_token, hash_password
from app.core.config import settings
from datetime import  timedelta
from app.schemas.token_schema import TokenResponseSchema


def create_token(user_id: str, role: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
    access_token = create_access_token(
                            user_id= str(user_id), role= role, expires_delta=access_token_expires
                        )
    refresh_token = create_refresh_token(
                            user_id=str(user_id), expires_delta=refresh_token_expires
                        )
    
    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires=access_token_expires,
        refresh_token_expires=refresh_token_expires
    )