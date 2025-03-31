# Defines Celery tasks.
from app import celery
from app.utils.fetch_br_recommendations import fetch_br_recommendations

@celery.task
def update_br_recommendations():
    fetch_br_recommendations()

# Add other tasks here...