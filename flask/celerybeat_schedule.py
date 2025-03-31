from celery.schedules import crontab

beat_schedule = {
    'run-fetch-surface': {
        'task': 'app.tasks.run_fetch_surface',
        'schedule': crontab(minute='*/5', hour='13-22', day_of_week='1-5'),
    },
}