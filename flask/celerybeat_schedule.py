# Correctly defines the task schedule.
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'update-br-recommendations': {
        'task': 'app.tasks.update_br_recommendations',
        'schedule': crontab(hour=22, minute=0, day_of_week='1-5'),
    },
    # Add other scheduled tasks here...
}