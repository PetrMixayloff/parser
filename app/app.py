import uvicorn
from fastapi import FastAPI
from app.worker.celery_worker import parse_task


app = FastAPI()


@app.post("/parse/{url}")
def post(url: str) -> str:
    """Добавление нового URL в задания для парсинга. URL в формате example.com"""

    req = parse_task.apply_async(args=[url])
    return req.id


if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=8000, reload=True)
