from fastapi import APIRouter, Depends, HTTPException, Path
from app.worker.tasks import parse_task
from .session import get_db
from sqlalchemy.orm import Session
from app.crud import get_result_by_id

api_router = APIRouter()


@api_router.post("/parse/{url}",
                 responses={
                     200: {
                         "description": "Добавление нового URL в задания для парсинга",
                         "content": {
                             "application/json": {
                                 "example": "77d05ad4-81ae-4c17-afb8-e8607a6656a9"
                             }
                         }}
                 })
def receive_task(url: str = Path(..., example="example.com")) -> str:
    req = parse_task.apply_async(args=[url])
    return req.id


@api_router.get("/results/{result_id}",
                responses={
                    200: {
                        "description": "Получение результата парсинга по идентификатору",
                        "content": {
                            "application/json": {
                                "example": '{"html": {"count":1, "nested":100}, '
                                           '"body":{"count":1, "nested":99}, "H1": {"count":2,"nested":0}'
                            }
                        }},
                    404: {
                        "description": "По заданному идентификатору ничего не найдено."
                    }
                })
def get_task_by_id(result_id: str = Path(..., example="77d05ad4-81ae-4c17-afb8-e8607a6656a9"),
                   db: Session = Depends(get_db)) -> str:
    res = get_result_by_id(db=db, result_id=result_id)
    if res is not None:
        return res.result
    raise HTTPException(
        status_code=404,
        detail="По заданному идентификатору ничего не найдено.",
    )
