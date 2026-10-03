
from app.db.base import get_db
from app.core.rate_limit import rate_limit
from sqlalchemy.orm import Session
from app.services import auth_service, token_service
from fastapi import APIRouter, Depends, Response
from app.schemas.base_schema import DataResponse
from app.schemas.token_schema import AccessTokenResponseSchema,RefreshTokenSchema
from app.schemas.auth_schema import LoginSchema, AuthResponseSchema, RegisterSchema

router = APIRouter()

@router.post("/login", tags=["auth"], description="Login and get access token", response_model=DataResponse[AuthResponseSchema], response_model_exclude_none=True)
async def login(
    data: LoginSchema, 
    response: Response, 
    db: Session = Depends(get_db), 
    _: None = Depends(rate_limit(scope="login", limit=5, window_seconds=60))
    ):
    return  auth_service.login(data, response, db)
    

@router.post("/register", tags=["auth"], description="Register a new user", response_model=DataResponse[AuthResponseSchema], response_model_exclude_none=True)
async def register(
    data: RegisterSchema, 
    response: Response, 
    db: Session = Depends(get_db),
    _: None = Depends(rate_limit(scope="register", limit=5, window_seconds=60))
    ):
    return  auth_service.register(data, response, db)


@router.post("/refresh-token", tags=["auth"], description="Refresh token", response_model=DataResponse[AccessTokenResponseSchema], response_model_exclude_none=True)
async def register(
    data: RefreshTokenSchema, 
    response: Response, 
    db: Session = Depends(get_db),
    _: None = Depends(rate_limit(scope="refresh_token", limit=20, window_seconds=60))
    ):
    return  token_service.refresh_token(data, response, db)




    