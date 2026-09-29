
from fastapi import FastAPI
from app.models.base_model import Base
from app.db.base import engine
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Tasky API',
    description='Task Management System',
    version='1.0.0'
)

app.include_router(user_router)
app.include_router(auth_router)

@app.get('/')
def root():
    return {'message': 'Welcome to Tasky API!'}