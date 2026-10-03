from pydantic import BaseModel
from datetime import timedelta

class RefreshTokenSchema(BaseModel):
    refresh_token: str
class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires: timedelta
    refresh_token_expires: timedelta

class AccessTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = 'Bear'