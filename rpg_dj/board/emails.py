from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post, User
from datetime import datetime, timedelta


def notify_request_accept(comment):
    post = comment.post
    to_email = comment.user.email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'Your request has been accepted on Best MMORPG Fun site'
    body = f'User {post.user} has accepted your request to post {post.head}'

    msg = EmailMessage(subject=subject, body=body, from_email=from_email, to=[to_email, ])

    return msg.send(fail_silently=True)


# email for new comments is in signals.py


def news_mail():
    emails = User.objects.all().values_list('email', flat=True)
    threshold = datetime.now() - datetime.timedelta(week=1)
    news = Post.objects.filter(time_in__gt=threshold)
    html_content = render_to_string('news_email.html', context={'news': news})
    text_content = render_to_string('news_email.html', context={'news': news})
    subject = 'Weekly news from Best MMORPG Fun site'
    body = text_content
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=emails)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

