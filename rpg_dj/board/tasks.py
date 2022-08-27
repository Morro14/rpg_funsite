from celery import shared_task
from .emails import news_mail


@shared_task(name='weekly_mail_task')
def weekly_mail_task():
    news_mail()
