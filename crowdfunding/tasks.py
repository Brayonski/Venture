from celery import *
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from crowdfunding.emails import *

logger = get_task_logger(__name__)


@task(name="send_approval_request_email_task")
def send_approval_request_email_task(campaign_name, campaign_id, subject, from_email, to):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent approval request email")
    return send_approval_request_email(campaign_name, campaign_id, subject, from_email, to)

@task(name="send_actioned_campaign_email_task")
def send_actioned_campaign_email_task(campaign_name, campaign_id, subject, from_email, to, status):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent Campaign admin response email")
    return send_actioned_campaign_email(campaign_name, campaign_id, subject, from_email, to, status)


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="task_close_due_campaigns", ignore_result=True)
def task_close_due_campaigns():
    print("Hi,im periodically running")
    logger.info("Saved image from Flickr")