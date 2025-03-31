from celery.schedules import crontab

beat_schedule = {
    'run-fetch-surface': {
        'task': 'app.tasks.run_fetch_surface',
        'schedule': crontab(minute='*/5', hour='13-22', day_of_week='1-5'),
    },

    'run-volatility-analysis': {
        'task': 'app.tasks.run_volatility_analysis',
        'schedule': crontab(minute='0', hour='22', day_of_week='1-5'),
    },
}