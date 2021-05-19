from celery import Celery


celery_app = Celery("worker",
                    broker="amqp://guest:guest@0.0.0.0:5672//",
                    include=['app.worker.tasks'])
