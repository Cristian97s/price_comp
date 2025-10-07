from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "scraper",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.scraper"],  # asegura que Celery encuentre las tareas
)

# Configuración adicional
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

if __name__ == "__main__":
    celery_app.start()