import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    USER: str = os.getenv("USER")
    PASSWORD: str = os.getenv("PASSWORD")
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    DBNAME: str = os.getenv("DBNAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE: int = int(os.getenv("ACCESS_TOKEN_EXPIRE"))
    REFRESH_TOKEN_EXPIRE: int = int(os.getenv("REFRESH_TOKEN_EXPIRE"))
    UPSTASH_REDIS_REST_URL: str = os.getenv("UPSTASH_REDIS_REST_URL")
    UPSTASH_REDIS_REST_TOKEN: str = os.getenv("UPSTASH_REDIS_REST_TOKEN")
    CORS_ORIGINS:str = os.getenv("CORS_ORIGINS")
settings = Settings()