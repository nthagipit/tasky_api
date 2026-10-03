
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.exception import AppException
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.cors import origins
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.task_router import router as task_router
from app.routers.task_detail_router import router as task_detail_router
from app.schemas.base_schema import DataResponse
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Tasky API',
    description='Task Management System',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(task_detail_router)

@app.exception_handler(AppException)
def handle_app_exception(request, exc):
    response_body = DataResponse.error(status_code=exc.status_code, detail=exc.message)
    if hasattr(response_body, "model_dump"):
        content = response_body.model_dump(exclude_none=True)  # Pydantic v2
    else:
        content = response_body.dict(exclude_none=True)
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=getattr(exc, "headers", None)
    )

@app.get('/')
def root():
    return {'message': 'Welcome to Tasky API!'}