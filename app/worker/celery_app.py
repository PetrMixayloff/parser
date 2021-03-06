from celery import Celery


celery_app = Celery("worker",
                    broker="amqp://guest:guest@queue:5672//",
                    include=['app.worker.tasks'])
