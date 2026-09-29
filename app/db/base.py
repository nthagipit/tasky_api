from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
from urllib.parse import quote_plus

user = quote_plus(str(settings.USER))
password = quote_plus(str(settings.PASSWORD))

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{settings.HOST}:{settings.PORT}/{settings.DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=1, max_overflow=2, pool_recycle=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

