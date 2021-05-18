from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .celery_app import celery_app
from celery.signals import worker_process_init, worker_process_shutdown
from app.config import settings
from app.crud import save_result, update_result

engine = None


@worker_process_init.connect
def init_worker(**kwargs):
    global engine
    print('Worker connect to DB')
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global engine
    if engine:
        engine.dispose()


@celery_app.task(bind=True)
def parse_task(self, url: str):
    print('incoming task')
    url = 'http://' + url
    task_id = self.request.id
    parse_obj = {
        'id': task_id,
        'url': url,
        'date': datetime.utcnow(),
        'result': 'В процессе'
    }
    with Session(engine) as session:
        save_result(db=session, obj=parse_obj)
    resp = requests.get(url, headers=settings.HEADERS, timeout=settings.TIMEOUT)
    soup = BeautifulSoup(resp.text, 'lxml')
    root = soup.html
    result = dict()
    result['html'] = len(root.contents)
    for tag in root.recursiveChildGenerator():
        if tag.name is None:
            continue
        if result.get(tag.name) is None:
            result[tag.name] = 0
        result[tag.name] += len(tag.contents)
    with Session(engine) as session:
        update_result(db=session, result_id=task_id, result=json.dumps(result))
