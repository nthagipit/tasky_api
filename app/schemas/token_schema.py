from pydantic import BaseModel
from datetime import timedelta

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires: timedelta
    refresh_token_expires: timedelta