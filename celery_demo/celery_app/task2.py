import time
from celery_app import app

@app.task
def multiply(x, y):
    time.sleep(30)
    return x * y
