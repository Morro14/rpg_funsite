import os
from django.conf import settings
import random

from django.core.mail import EmailMessage


def signup_email(email, code):
    email_subject = "Conformation e-mail for signing-up for Best MMORPG Fun-site"
    email_body = '<a href=""> "Use this link to confirm that you are signing up with this e-mail" </a> '
    msg = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=os.getenv("EMAIL_HOST"),
        to=email,
    )
    return msg.send(fail_silently=True)


def send_registration_code(email, code):
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'Verification code for registration on Best MMORPG fun site'
    body = f'Verification code: {code}'
    msg = EmailMessage(subject=subject, body=body, from_email=from_email, to=[email])
    msg.send(fail_silently=True)
    return code



