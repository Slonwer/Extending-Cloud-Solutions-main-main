from celery import Celery

app = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',   # ou pyamqp://guest@localhost// para RabbitMQ
    backend='redis://localhost:6379/0'
)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)
