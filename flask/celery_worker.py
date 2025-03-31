# Properly initializes the Celery app.
from app import create_app
app, celery = create_app()