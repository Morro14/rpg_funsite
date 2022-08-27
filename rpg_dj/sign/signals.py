from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OneTimeCode
from .tasks import delete_one_time_codes_task


@receiver(post_save, sender=OneTimeCode)
def one_time_code_delete(created, instance, **kwargs):
    if created:
        code_pk = instance.pk
        print(code_pk)
        delete_one_time_codes_task.apply_async([code_pk], countdown=6)

