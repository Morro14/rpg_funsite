from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from django.core.mail import EmailMessage
import os


@receiver(post_save, sender=Comment)
def notify_new_comment(created, instance, **kwargs):
    if created:
        user = instance.post.user
        email = user.email
        link = f'http://127.0.0.1:8000/board/posts/{instance.post.pk}'
        subject = 'Someone left a comment to your post on Best MMORPG Fun site'
        body = f'A new comment to your {instance.post.head} post:\n' \
               f'{instance.text} \n' \
               f'Link: {link}'

        msg = EmailMessage(body=body, subject=subject, from_email=os.getenv("EMAIL"), to=[email])
        msg.send(fail_silently=False)




