import os
import sys

from celery import Celery
from celery.schedules import crontab

from config import Config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) 

celery = Celery("trekking", broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
celery.conf.beat_schedule = {
    "send-daily-reminders": {
        "task": "tasks.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),  # every day at 8:00 AM
    },
    "generate-monthly-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),  # every month on the 1st at 12:00 AM
    },
}


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        from app import app  

        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

import tasks 
