from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import strip_tags

@shared_task
def send_notification(title, body, EMAIL_HOST_USER, emails):
    return send_mail(title, strip_tags(body), EMAIL_HOST_USER, emails, html_message=body)