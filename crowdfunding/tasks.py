from celery import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.utils import timezone
from datetime import date,datetime
from crowdfunding.models import *
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
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


@task(name="send_mpesa_stk_task")
def send_mpesa_stk_task(phone,amount):
    logger.info("send mpesa stk task")
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y%m%d%H%M%S")
    consumer_key = "G4fR8iS27KSOwAJ5eOtRq0MFdwDVbwau"
    consumer_secret = "BrPh8l8ZbpCQAoUt"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    responseTokenData = json.loads(responseToken.text)
    accessToken = responseTokenData["access_token"]
    shortCode = "174379"
    passKey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    passwordMpesa = shortCode + passKey + formatedDate
    encodedBytes = base64.b64encode(passwordMpesa.encode("utf-8"))
    encodedStr = str(encodedBytes).encode("utf-8")
    checkoutResponse = ''

    if accessToken is not None:
        access_token = accessToken
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": shortCode,
            "Password": encodedStr,
            "Timestamp": formatedDate,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(amount),
            "PartyA": phone,
            "PartyB": shortCode,
            "PhoneNumber": phone,
            "CallBackURL": "http://52.37.84.193:8081/crowdfunding/mpesa_checkout_response",
            "AccountReference": "ACCOUNT01",
            "TransactionDesc": "VENTURELIFTDONATION"
        }

        response = requests.post(api_url, json=request, headers=headers)
        checkoutResponse = response.text

    return "STK PUSH Done"


@periodic_task(run_every=(crontab(minute=0, hour=0)), name="task_close_due_campaigns", ignore_result=True)
def task_close_due_campaigns():
    print("Hi,im periodically running")
    due_campaigns = Campaign.objects.filter(duration__lte=date.today(),campaign_status='APPROVED')
    for campaign in due_campaigns:
        campaign.campaign_status = "CLOSED"
        campaign.save()
        subject, from_email, to = 'Closed Campaign Disbursement Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
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
            disbursement = CampaignDisbursement(campaign=campaign, campaign_target=campaign.target_amount, created_at=timezone.now(), amount=campaign.total_funds_received,
                                                disbursement_type='REFUND', disbursement_status='PENDING',
                                                recipient=campaign.campaign_owner,
                                                recipient_email=campaign.company_email, approval_status='PENDING', approved=False, rejected=False,
                                                disbursed=False)
            disbursement.save()
            send_campaign_disbursement_email_task.delay(campaign.campaign_name, campaign.id, subject, from_email, to, "refunds")

    logger.info("Saved disbursement for closed campaigns")