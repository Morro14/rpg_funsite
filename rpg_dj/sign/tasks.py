from celery import shared_task
from .util import code_delete


@shared_task(name="delete_one_time_codes_task")
def delete_one_time_codes_task(code_pk):
    print(code_pk)
    code_delete(code_pk)


