import os

from celery import Celery
from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

# Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import views
from app import models
