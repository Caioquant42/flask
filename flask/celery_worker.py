from app import create_app
from celery import Celery

flask_app = create_app()

celery = Celery(flask_app.name)
celery.conf.update(flask_app.config)

# Check if the configuration is loaded
print("Flask app config:", flask_app.config)

# Use get() method with a default value to avoid KeyError
celery.conf.broker_url = flask_app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = flask_app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

print("Celery Broker URL:", celery.conf.broker_url)
print("Celery Result Backend:", celery.conf.result_backend)