import requests
from bs4 import BeautifulSoup
from .celery_app import celery_app

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
TIMEOUT = 5


@celery_app.task(bind=True)
def parse_task(url: str) -> str:
    url = 'http://' + url
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
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
