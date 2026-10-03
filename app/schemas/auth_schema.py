from pydantic import BaseModel, EmailStr, Field

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):
    email: EmailStr = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=255)


class AuthResponseSchema(BaseModel):
    access_token: str
    expires_access_token: int
    refresh_token: str
    expires_refresh_token: int
    token_type: str = "Bearer"

