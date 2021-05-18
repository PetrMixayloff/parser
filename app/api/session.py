from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db is not None:
            db.close()
