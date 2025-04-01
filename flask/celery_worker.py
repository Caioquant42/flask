from app import create_app
from celery import Celery
from celerybeat_schedule import beat_schedule  # Add this import

# Unpack the tuple returned by create_app()
flask_app, _ = create_app()

celery = Celery(flask_app.name)
celery.conf.update(flask_app.config)

# Check if the configuration is loaded
print("Flask app config:", flask_app.config)

# Use the new configuration keys, falling back to the old ones if not present
celery.conf.broker_url = flask_app.config.get('broker_url') or flask_app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = flask_app.config.get('result_backend') or flask_app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Explicitly set the beat_schedule
celery.conf.beat_schedule = beat_schedule

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

print("Celery Broker URL:", celery.conf.broker_url)
print("Celery Result Backend:", celery.conf.result_backend)
print("Beat Schedule:", celery.conf.beat_schedule)

# Make sure you're only exporting the celery app
if __name__ == '__main__':
    celery.start()