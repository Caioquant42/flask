import os
from celerybeat_schedule import CELERYBEAT_SCHEDULE

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERYBEAT_SCHEDULE = CELERYBEAT_SCHEDULE