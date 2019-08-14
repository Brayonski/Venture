from celery import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.utils import timezone
from datetime import date
from crowdfunding.models import *
from venturelift_profiles.models import *
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
from crowdfunding.emails import *
from datetime import datetime
import uuid
import decimal
from django.utils.timezone import utc
from time import sleep
from django.utils.crypto import get_random_string

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


@task(name="send_mpesa_c2b_notification_url_task")
def send_mpesa_c2b_notification_url_task(accountName,referenceCode,amount,phone,shortCode):
    checkPayment = MpesaSTKPush.objects.filter(name=accountName).first()
    if checkPayment:
        stkPush = MpesaSTKPush.objects.get(name=accountName)
        c2bNotification = MpesaC2BNotification(payment=stkPush.payment, created_at=timezone.now(),
                                               account_name=accountName, amount_received=amount, phone_number=phone,
                                               reference_code=referenceCode, shortcode=shortCode)
        c2bNotification.save()
        stkPush.payment.payment_status = 'PAID'
        stkPush.payment.paid = True
        stkPush.payment.save()

        totalReceived = stkPush.payment.campaign.total_funds_received + decimal.Decimal(amount)
        stkPush.payment.campaign.total_funds_received = totalReceived
        stkPush.payment.campaign.save()

        campaign_data = Campaign.objects.get(id=stkPush.payment.campaign.id)
        if campaign_data:
            logger.info(str(decimal.Decimal(amount)))
            logger.info(str(totalReceived))
            totalReceived = campaign_data.total_funds_received + decimal.Decimal(amount)
            campaign_data.total_funds_received = totalReceived
            campaign_data.save()
            logger.info("After Received")
            logger.info(str(totalReceived))

            if campaign_data.campaign_type == "REWARD BASED":
                if amount >= campaign_data.campaign_reward_threshold:
                    create_reward = CampaignReward(campaign=campaign_data, payment=stkPush.payment,
                                                   created_at=timezone.now(),
                                                   rewarded_user_email=stkPush.payment.donator_email,
                                                   reward=campaign_data.campaign_reward_details,
                                                   reward_status="PENDING")
                    create_reward.save()

    return "C2B Notification Received"

@task(name="send_mpesa_c2b_register_url_task")
def send_mpesa_c2b_register_url_task():
    try:
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        api_URL = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        accessToken = ''

        tokenFetch = MpesaApiToken.objects.filter(status='ACTIVE').first()
        if tokenFetch:
            tokenGet = MpesaApiToken.objects.get(status='ACTIVE')
            now = datetime.utcnow().replace(tzinfo=utc)
            timediff = now - tokenGet.created_at
            if (timediff.total_seconds() < 3500):
                accessToken = tokenGet.token
            else:
                tokenGet.status = 'INACTIVE'
                tokenGet.save()
                responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                responseTokenData = json.loads(responseToken.text)
                accessToken = responseTokenData["access_token"]
                saveToken = MpesaApiToken(token=accessToken, created_at=datetime.now(), status='ACTIVE')
                saveToken.save()
        else:
            responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
            responseTokenData = json.loads(responseToken.text)
            accessToken = responseTokenData["access_token"]
            saveToken = MpesaApiToken(token=accessToken, created_at=datetime.now(), status='ACTIVE')
            saveToken.save()

        sleep(5)
        headers = {"Authorization": "Bearer %s" % accessToken}
        request = {"ShortCode": " ",
                   "ResponseType": " ",
                   "ConfirmationURL": "http://52.37.84.193:8081/crowdfunding/confirmation_url",
                   "ValidationURL": "http://52.37.84.193:8081/crowdfunding/validation_url"}

        response = requests.post(api_URL, json=request, headers=headers)
        checkoutResponse = response.text
        c2bRegister = MpesaC2BRegister(name='Register C2B URL', created_at=timezone.now(),
                                       request_json=json.dumps(request),
                                       response_json=response.text, response_code=response.status_code)
        c2bRegister.save()
        logger.info(checkoutResponse)
        return "C2B Notification Url Registered"
    except requests.exceptions.ConnectionError:
        errorText = "Connection refused"
        logger.info(errorText)



@task(name="send_mpesa_stk_task")
def send_mpesa_stk_task(phone,amount,accountName,paymentId):
    try:
        payment = CampaignPayment.objects.get(id=paymentId)
        if payment:
            logger.info("send mpesa stk task")
            myDate = datetime.now()
            formatedDate = myDate.strftime("%Y%m%d%H%M%S")
            consumer_key = settings.CONSUMER_KEY
            consumer_secret = settings.CONSUMER_SECRET
            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            accessToken = ''

            tokenFetch = MpesaApiToken.objects.filter(status='ACTIVE').first()
            if tokenFetch:
                tokenGet = MpesaApiToken.objects.get(status='ACTIVE')
                now = datetime.utcnow().replace(tzinfo=utc)
                timediff = now - tokenGet.created_at
                if (timediff.total_seconds() < 3500):
                    accessToken = tokenGet.token
                else:
                    tokenGet.status = 'INACTIVE'
                    tokenGet.save()
                    responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                    responseTokenData = json.loads(responseToken.text)
                    accessToken = responseTokenData["access_token"]
                    saveToken = MpesaApiToken(token=accessToken, created_at=datetime.now(), status='ACTIVE')
                    saveToken.save()
            else:
                responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                responseTokenData = json.loads(responseToken.text)
                accessToken = responseTokenData["access_token"]
                saveToken = MpesaApiToken(token=accessToken, created_at=datetime.now(), status='ACTIVE')
                saveToken.save()

            sleep(5)
            shortCode = settings.SHORTCODE
            passKey = settings.PASS_KEY
            passwordMpesa = shortCode + passKey + formatedDate
            encodedBytes = base64.b64encode(passwordMpesa.encode("utf-8"))
            encodedStr = str(encodedBytes).encode("utf-8")
            checkoutResponse = ''

            if accessToken is not None:
                phoneNumber = phone.strip()
                if phoneNumber[:2] == '07':
                    phoneNumber = '254' + phoneNumber[1:]
                elif phoneNumber[:1] == '+':
                    phoneNumber = phoneNumber[1:]
                elif phoneNumber[:1] == '7':
                    phoneNumber = '254' + phoneNumber[0:]

                access_token = accessToken
                api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                headers = {"Authorization": "Bearer %s" % access_token}
                request = {
                    "BusinessShortCode": shortCode,
                    "Password": encodedStr,
                    "Timestamp": formatedDate,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": str(amount),
                    "PartyA": phoneNumber,
                    "PartyB": shortCode,
                    "PhoneNumber": phoneNumber,
                    "CallBackURL": "http://52.37.84.193:8081/crowdfunding/mpesa_checkout_response",
                    "AccountReference": accountName,
                    "TransactionDesc": "VENTURELIFTDONATION"
                }

                response = requests.post(api_url, json=request, headers=headers)
                checkoutResponse = response.text
                responseSTKData = json.loads(checkoutResponse)
                stkPush = MpesaSTKPush(name=accountName, payment=payment, created_at=timezone.now(),
                                       request_json=json.dumps(request), response_json=response.text,
                                       response_code=response.status_code,checkoutID=responseSTKData['CheckoutRequestID'])
                stkPush.save()
                logger.info(checkoutResponse)
                logger.info(phoneNumber)
            return "STK PUSH Done"
    except requests.exceptions.ConnectionError:
        errorText = "Connection refused"
        logger.info(errorText)


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


@periodic_task(run_every=(crontab(minute='*/5')), name="task_survey_users", ignore_result=True)
def task_survey_users():
    print("Hi,im survey user periodically running")
    surveys = SurveyUser.objects.filter(active=True)
    now = datetime.utcnow().replace(tzinfo=utc)
    for survey in surveys:
        if now >= survey.to_time:
            unique_id = get_random_string(length=32)
            survey.user.set_password(unique_id)
            survey.user.save()
            survey.active = False
            survey.save()

