from celery import task
from celery.utils.log import get_task_logger
from django.utils import timezone
from datetime import date
from crowdfunding.models import *
from django.conf import settings

from venturelift_profiles.emails import *

logger = get_task_logger(__name__)


@task(name="send_business_connect_request_email_task")
def send_business_connect_request_email_task(business, investor, subject, from_email, to):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent connect request email")
    return send_business_connect_request_email(business, investor, subject, from_email, to)


@task(name="send_investor_approved_connect_email_task")
def send_investor_approved_connect_email_task(business, investor, subject, from_email, to):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent approved connect email to investor")
    return send_investor_approved_connect_email(business, investor, subject, from_email, to)