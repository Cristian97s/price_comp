from celery import Celery
import os

# URL de Redis (broker)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "scraper",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_routes={
        "app.tasks.scraper.*": {"queue": "scraper"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
