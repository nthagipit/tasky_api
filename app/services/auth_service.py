from fastapi import Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.user_model import User
from app.models.refresh_token_model import RefreshToken
from app.schemas.auth_schema import AuthResponseSchema, LoginSchema
from app.schemas.base_schema import DataResponse
from app.services.token_service import create_token
from app.core.security import  hash_password, verify_password
from app.schemas.auth_schema import RegisterSchema
from app.core.logging import logging

logger = logging.getLogger("app.services.core_service_client")


def login(data: LoginSchema, response: Response, db: Session ):
    
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user or not verify_password(
        data.password,
        user.hashed_password,
    ):
        logger.warning(f"Failed login attempt for email: {data.email}")
        response.status_code = 401
        return DataResponse.error(status_code=401,detail="Invalid email or password",)
    
    token = create_token(user.id, user.role)

    refresh_token_record = RefreshToken(
        token_hash=hash_password(token.refresh_token),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc)
        + token.refresh_token_expires,
    )

    try:
        db.add(refresh_token_record)
        db.commit()

    except Exception:
        db.rollback()
        raise

    data_response = AuthResponseSchema(
        id=str(user.id),
        email=user.email,
        access_token=token.access_token,
        expires_access_token=token.access_token_expires.total_seconds(), # Convert minutes to seconds
        refresh_token=token.refresh_token,
        expires_refresh_token=token.refresh_token_expires.total_seconds(),  # Convert days to seconds
        token_type="Bearer",
    )

    return DataResponse.custom_response("200",data=data_response,message="Login successful")


def register(data: RegisterSchema, response: Response, db: Session):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        logger.warning(f"Attempt to register with existing email: {data.email}")
        response.status_code = 400
        return DataResponse.error(status_code=400, detail="User already exists")   

    try:

        db_user = User(email=data.email, hashed_password=hash_password(data.password))
        db.add(db_user)
        db.flush()

        token = create_token(db_user.id, db_user.role)

        refresh_token_record = RefreshToken(
            token_hash=hash_password(token.refresh_token), 
            user_id=str(db_user.id), 
            expires_at=datetime.now(timezone.utc) + token.refresh_token_expires
        )
            
        db.add(refresh_token_record)
        db.commit()

        data_response = AuthResponseSchema(
            id=str(db_user.id),
            email=db_user.email,
            access_token=token.access_token,
            expires_access_token=token.access_token_expires.total_seconds(), # Convert minutes to seconds
            refresh_token=token.refresh_token,
            expires_refresh_token=token.refresh_token_expires.total_seconds(),  # Convert days to seconds
            token_type="Bearer",
        )

        return DataResponse.custom_response("201",data=data_response, message="User created successfully")
    
    except Exception as e:
            db.rollback()
            response.status_code = 400
            logger.error(f"Error creating user: {str(e)}")
            return DataResponse.error(status_code=400, detail="Error creating user")
