from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .celery_app import celery_app
from sqlalchemy import create_engine
from app.config import settings
from app.crud import save_result, update_result


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


@celery_app.task(bind=True)
def parse_task(self, url: str):
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
        result['html'] = {'count': 1, 'nested': len(root.contents)}
        for tag in root.recursiveChildGenerator():
            if tag.name is None:
                continue
            if result.get(tag.name) is None:
                result[tag.name] = {'count': 0, 'nested': 0}
            result[tag.name]['count'] += 1
            result[tag.name]['nested'] += len(tag.contents)
        update_result(db=session, result_id=task_id, result=json.dumps(result))
