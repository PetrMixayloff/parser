from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import contextmanager

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def db_session_scope():
    """Provide a transactional scope around a series of operations."""
    db = Session()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()


def get_db() -> Session:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db is not None:
            db.close()
