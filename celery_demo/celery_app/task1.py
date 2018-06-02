import time
from celery_app import app

@app.task
def add(x, y):
    time.sleep(20)
    return x + y
