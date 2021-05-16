from celery import Celery


celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.celery_worker.parse_task": "main-queue"}

celery_app.conf.update(task_track_started=True)
