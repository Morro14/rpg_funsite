import os
from celery.schedules import crontab
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpg_dj.settings")

app = Celery("rpg_dj")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'task weekly': {
        'task': 'weekly_mail_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#        'schedule': 10,
        'args': (),
    }
}

