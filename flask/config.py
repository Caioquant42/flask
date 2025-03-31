import os
from celerybeat_schedule import beat_schedule

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    broker_url = 'redis://localhost:6379/0'
    RESULT_BACKEND = 'redis://localhost:6379/0'
    # Keep the old keys for backwards compatibility
    CELERY_broker_url = broker_url
    result_backend = RESULT_BACKEND
    beat_schedule = beat_schedule
    broker_connection_retry_on_startup = True