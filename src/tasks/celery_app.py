from celery import Celery

from src.config import settings

celery_instance = Celery("tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"])

celery_instance.conf.beat_schedule = {
    "zadachi": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}

"""
для запуска воркера на винде:
celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo

src.tasks.celery_app
путь до места, где лежит объект класса celery_instance

worker
что именно запускаем

-l INFO
уровень логов

--pool=solo
пул потоков, обязательно при запуске в винде


для запуска бит на винде:
запуск в 3-х терминалах
1. запуск самого приложения fastsapi
2. запуск воркера: celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo
3. запуск бит: celery -A src.tasks.celery_app:celery_instance beat -l INFO

"""
