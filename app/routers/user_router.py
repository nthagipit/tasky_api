
from fastapi import APIRouter, Depends
from app.db.base import get_db
from app.middlewares.authenticate import require_roles
from app.models.user_model import User
from app.schemas.user_schema import  UserSchema
from app.schemas.base_schema import DataResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("", description="Get all users", response_model=DataResponse[list[UserSchema]])
async def get_users(current_user: User = Depends(require_roles("ADMIN")), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return DataResponse.custom_response("200",data=users, message="Users retrieved successfully")



