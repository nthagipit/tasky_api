
from fastapi import APIRouter, Depends, Response
from app.schemas.auth_schema import LoginSchema, AuthResponseSchema, RegisterSchema
from app.schemas.base_schema import DataResponse
from app.db.base import get_db
from sqlalchemy.orm import Session
from app.services import auth_service

router = APIRouter()

@router.post("/login", tags=["auth"], description="Login and get access token", response_model=DataResponse[AuthResponseSchema], response_model_exclude_none=True)
async def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    return  auth_service.login(data, response, db)
    

@router.post("/register", tags=["auth"], description="Register a new user", response_model=DataResponse[AuthResponseSchema], response_model_exclude_none=True)
async def register(data: RegisterSchema, response: Response, db: Session = Depends(get_db)):
    return  auth_service.register(data, response, db)

    
    




    