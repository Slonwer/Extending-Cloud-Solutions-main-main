from celery_app.tasks import add

result = add.delay(4, 5)
print("Resultado:", result.get(timeout=10))
