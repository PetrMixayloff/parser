from fastapi import APIRouter, Depends
from app.worker.celery_worker import parse_task

api_router = APIRouter()


@api_router.post("/parse/{url}")
def post(url: str) -> str:
    """Добавление нового URL в задания для парсинга. URL в формате example.com"""

    req = parse_task.apply_async(args=[url])
    return req.id
