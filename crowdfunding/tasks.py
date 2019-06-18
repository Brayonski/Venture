from celery import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.utils import timezone
from datetime import date
from crowdfunding.models import *
from django.conf import settings

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

@task(name="send_campaign_disbursement_email_task")
def send_campaign_disbursement_email_task(campaign_name, campaign_id, subject, from_email, to, status):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent Campaign funds disbursement email")
    return send_campaign_disbursement_email(campaign_name, campaign_id, subject, from_email, to, status)


@periodic_task(run_every=(crontab(minute='*/5')), name="task_close_due_campaigns", ignore_result=True)
def task_close_due_campaigns():
    print("Hi,im periodically running")
    due_campaigns = Campaign.objects.filter(duration__lte=date.today(),campaign_status='APPROVED')
    for campaign in due_campaigns:
        campaign.campaign_status = "CLOSED"
        campaign.save()
        subject, from_email, to = 'Closed Campaign Disbursement Request', settings.EMAIL_HOST_USER, campaign.campaign_owner.email
        if campaign.total_funds_received >= campaign.target_amount:
            fees = CampaignConfiguration.objects.get(name='Configurations')
            funds = campaign.total_funds_received
            processing_fee_amount = 0
            if fees.processing_fee_type == "Percentage":
                fee_percent = fees.processing_fee / 100
                processing_fee_amount = funds * fee_percent
            else:
                processing_fee_amount = fees.processing_fee

            funds_to_disburse = funds - processing_fee_amount
            disbursement = CampaignDisbursement(campaign=campaign, campaign_target=campaign.target_amount, created_at=timezone.now(),campaign_duration=campaign.duration, amount=funds_to_disburse, disbursement_type='DISBURSE', disbursement_status='PENDING', recipient=campaign.campaign_owner, recipient_email=campaign.company_email, approval_status='PENDING', approved=False, rejected=False, disbursed=False )
            disbursement.save()
            send_campaign_disbursement_email_task.delay(campaign.campaign_name, campaign.id, subject, from_email, to, "disbursements")
        else:
            disbursement = CampaignDisbursement(campaign=campaign, created_at=timezone.now(), amount=campaign.total_funds_received,
                                                disbursement_type='REFUND', disbursement_status='PENDING',
                                                recipient=campaign.campaign_owner,
                                                recipient_email=campaign.company_email, approval_status='PENDING', approved=False, rejected=False,
                                                disbursed=False)
            disbursement.save()
            send_campaign_disbursement_email_task.delay(campaign.campaign_name, campaign.id, subject, from_email, to, "refunds")

    logger.info("Saved disbursement for closed campaigns")