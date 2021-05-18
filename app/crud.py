from typing import Optional
from app.models import ParseResults
from sqlalchemy.orm import Session


def save_result(db: Session, obj: dict):
    result = ParseResults(**obj)
    db.add(result)
    db.commit()


def update_result(db: Session, result_id: str, result: str):
    result_obj = db.query(ParseResults).filter(ParseResults.id == result_id).first()
    if result_obj is not None:
        setattr(result_obj, 'result', result)
        db.commit()


def get_result_by_id(db: Session, result_id: str) -> Optional[ParseResults]:
    return db.query(ParseResults).filter(ParseResults.id == result_id).first()
