# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

from crowdfunding.forms import *
from .models import Campaign, CampaignSector
from venturelift_profiles.models import Business,AllSystemUser
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from crowdfunding.tasks import *
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import decimal

# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated() and not (request.user.business_creator.exists()) and not (
            request.user.supporter_creator.exists()) and not (request.user.investor_creator.exists()):
        return redirect(reverse('profile_create'))

    campaign_list = Campaign.objects.filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()
    template = loader.get_template('crowdfunding/investor/index.html')

    if request.user.is_authenticated() and request.user.business_creator.exists():
            campaign_list = Campaign.objects.filter(campaign_owner=request.user).order_by('-created_at')
            template = loader.get_template('crowdfunding/business/index.html')

    context = {
        'campaign_list': campaign_list,
        'campaign_sectors': campaign_sectors
    }
    return HttpResponse(template.render(context, request))


def crowdfunderindex(request):
    campaign_list = Campaign.objects.filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()
    template = loader.get_template('crowdfunding/investor/crowdfunder_index.html')

    context = {
        'campaign_list': campaign_list,
        'campaign_sectors': campaign_sectors
    }
    return HttpResponse(template.render(context, request))


@login_required
def business_campaign_view(request, campaign_id):
    campaign_data = Campaign.objects.get(id=campaign_id)
    campaign_sectors = CampaignSector.objects.all()
    template = loader.get_template('crowdfunding/business/view_campaign.html')

    context = {
        'campaign_data': campaign_data,
        'campaign_sectors': campaign_sectors,
    }
    return HttpResponse(template.render(context, request))


@login_required
def filter_campaign_view(request):
    if request.user.is_authenticated() and not (request.user.business_creator.exists()) and not (
            request.user.supporter_creator.exists()) and not (request.user.investor_creator.exists()):
        return redirect(reverse('profile_create'))

    template = loader.get_template('crowdfunding/investor/index.html')
    campaign_data = Campaign.objects.filter(campaign_name__contains=request.POST['campaign_name'],campaign_status='APPROVED')

    if request.user.is_authenticated() and request.user.business_creator.exists():
        template = loader.get_template('crowdfunding/business/index.html')
        campaign_data = Campaign.objects.filter(campaign_name__contains=request.POST['campaign_name'],campaign_owner=request.user)
    if empty(request.POST['sector']):
        sector_data = CampaignSector.objects.filter(id=request.POST['sector'])
        if request.user.is_authenticated() and request.user.business_creator.exists():
            campaign_data = Campaign.objects.filter(Q(sector=sector_data) | Q(campaign_name__contains=request.POST['campaign_name'])).filter(campaign_owner=request.user)
        else:
            campaign_data = Campaign.objects.filter(Q(sector=sector_data) | Q(campaign_name__contains=request.POST['campaign_name'])).filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()

    context = {
        'campaign_list': campaign_data,
        'campaign_sectors': campaign_sectors
    }
    return HttpResponse(template.render(context, request))


def crowdfunder_filter_campaign_view(request):
    template = loader.get_template('crowdfunding/investor/crowdfunder_index.html')
    campaign_data = Campaign.objects.filter(campaign_name__contains=request.POST['campaign_name'],campaign_status='APPROVED')

    if empty(request.POST['sector']):
        sector_data = CampaignSector.objects.filter(id=request.POST['sector'])
        campaign_data = Campaign.objects.filter(Q(sector=sector_data) | Q(campaign_name__contains=request.POST['campaign_name'])).filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()

    context = {
        'campaign_list': campaign_data,
        'campaign_sectors': campaign_sectors
    }
    return HttpResponse(template.render(context, request))

def empty(value):
    try:
        value = int(value)
    except ValueError:
        pass
    return bool(value)

class CreateCampaignView(LoginRequiredMixin, CreateView):
    template_name = 'crowdfunding/business/create_campaign.html'
    form_class = CreateCampaignForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = timezone.now()
        self.object.total_funds_received = 0
        self.object.campaign_status = 'OPENED'
        self.object.funds_disbursement_status = 'PENDING'
        self.object.campaign_owner = self.request.user
        self.object.approval_status = "PENDING"
        self.object.approved = False
        self.object.rejected = False
        self.object.save()

        #campaign_path = reverse('admin:campaign', args=(self.object.id,))

        subject, from_email, to = 'Campaign Approval Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
        send_approval_request_email_task.delay(self.object.campaign_name, self.object.id, subject, from_email, to)

        return redirect(reverse('crowdfunding:index'))

    def form_invalid(self, form):
        errors = form.errors
        raise Exception(errors)


@login_required
def create_donation(request, campaign_id):
    campaign_data = Campaign.objects.get(id=campaign_id)
    template = loader.get_template('crowdfunding/investor/create_payment.html')

    context = {
        'campaign_data': campaign_data,
    }
    return HttpResponse(template.render(context, request))


def crowdfunder_create_donation(request, campaign_id):
    campaign_data = Campaign.objects.get(id=campaign_id)
    template = loader.get_template('crowdfunding/investor/crowdfunder_create_payment.html')

    context = {
        'campaign_data': campaign_data,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def get_online_checkout_response(request):
    stkResponse = MpesaSTKResponse(name='STK Response',created_at=timezone.now(),response_json=request.body)
    stkResponse.save()
    data = json.loads(request.body)
    dataResponse = data['Body']['stkCallback']
    responseCode = dataResponse['ResultCode']
    if responseCode == 0:
        referenceCode = ''
        amount = ''
        phone = ''
        shortCode = settings.SHORTCODE
        checkoutId = dataResponse['CheckoutRequestID']
        callbackMetaData = dataResponse['CallbackMetadata']['Item']
        for item in callbackMetaData:
            if item['Name'] == "Amount":
                amount = str(item['Value'])
            if item['Name'] == "MpesaReceiptNumber":
                referenceCode = item['Value']
            if item['Name'] == "PhoneNumber":
                phone = item['Value']
        checkCheckout = MpesaSTKPush.objects.filter(checkoutID=checkoutId).first()
        if checkCheckout:
            checkout = MpesaSTKPush.objects.get(checkoutID=checkoutId)
            send_mpesa_c2b_notification_url_task.delay(checkout.name, referenceCode, amount, phone, shortCode)

    response = '{"success":"true","message":"Received"}'
    return HttpResponse(response)


@csrf_exempt
def confirmation_url(request):
    data = json.loads(request.body)
    accountName = data['BillRefNumber']
    referenceCode = data['TransID']
    amount = data['TransAmount']
    phone = data['MSISDN']
    shortCode = data['BusinessShortCode']
    #send_mpesa_c2b_notification_url_task.delay(accountName,referenceCode,amount,phone,shortCode)
    response = '{"success":"true","message":"Received"}'
    return HttpResponse(response)


@csrf_exempt
def validation_url(request):
    response = '{"success":"true","message":"Verified"}'
    return HttpResponse(response)


def register_url(request):
    send_mpesa_c2b_register_url_task.delay()
    response = '{"success":"true","message":"Verified"}'
    return HttpResponse(response)



@login_required
def make_payment(request):
    if request.user.is_authenticated() and not (request.user.business_creator.exists()) and not (
            request.user.supporter_creator.exists()) and not (request.user.investor_creator.exists()):
        return redirect(reverse('profile_create'))
    campaign_selected = Campaign.objects.get(id=request.POST['campaign_id'])
    payment = CampaignPayment(campaign=campaign_selected,created_at=timezone.now(),donator=request.user,donator_email=request.user.email,donator_phoneno=request.POST['donator_phoneno'],amount=request.POST['amount'],payment_method=request.POST['payment_method'],payment_status='INITIATED',paid=False,comments=request.POST['comments'],allow_visibility=request.POST['allow_visibility'])
    payment.save()
    template = loader.get_template('crowdfunding/investor/index.html')
    campaign_data = Campaign.objects.filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()

    context = {
        'campaign_list': campaign_data,
        'campaign_sectors': campaign_sectors,
        'message': 'Payment Initiated For Campaign '+campaign_selected.campaign_name+'. Please Check Your Phone For The STK-Push'
    }
    accountName = request.user.username + str(payment.pk)
    send_mpesa_stk_task.delay(request.POST['donator_phoneno'],request.POST['amount'],accountName.upper(),payment.pk)
    return HttpResponse(template.render(context, request))


def crowdfunder_make_payment(request):
    campaign_selected = Campaign.objects.get(id=request.POST['campaign_id'])
    payment = CampaignPayment(campaign=campaign_selected,created_at=timezone.now(),donator_email=request.POST['donator_email'],donator_phoneno=request.POST['donator_phoneno'],amount=request.POST['amount'],payment_method=request.POST['payment_method'],payment_status='INITIATED',paid=False,comments=request.POST['comments'],allow_visibility=request.POST['allow_visibility'])
    payment.save()
    template = loader.get_template('crowdfunding/investor/crowdfunder_index.html')
    campaign_data = Campaign.objects.filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()

    checkUser = AllSystemUser.objects.filter(email=request.POST['donator_email']).exists()
    if checkUser is False:
        createUser = AllSystemUser(created_at=timezone.now(),username=request.POST['donator_email'],email=request.POST['donator_email'],user_type='Crowdfunder')
        createUser.save()

    context = {
        'campaign_list': campaign_data,
        'campaign_sectors': campaign_sectors,
        'message': 'Payment Initiated For Campaign '+campaign_selected.campaign_name+'. Please Check Your Phone For The STK-Push'
    }
    accountName = "ANNONYMUS" + str(payment.pk)
    send_mpesa_stk_task.delay(request.POST['donator_phoneno'],request.POST['amount'],accountName.upper(),payment.pk)
    return HttpResponse(template.render(context, request))

@csrf_exempt
def verify_paypal_payment_funder(request):
    data = json.loads(request.body)
    campaign_selected = Campaign.objects.get(id=data['campaignID'])
    payment = CampaignPayment(campaign=campaign_selected, created_at=timezone.now(),
                              donator_email=data['donatorEmail'],
                              donator_phoneno=data['donatorPhone'], amount=data['amount'],
                              payment_method=data['paymentMethod'], payment_status='PAID', payment_order_number=data['orderID'], payment_payer_id=data['payerID'], paid=True,
                              comments=data['comments'], allow_visibility=data['allowVisibility'])
    payment.save()
    totalReceived = campaign_selected.total_funds_received + decimal.Decimal(data['amount'])
    campaign_selected.total_funds_received = totalReceived
    campaign_selected.save()
    if campaign_selected.campaign_type == "REWARD BASED":
        if data['amount'] >= campaign_selected.campaign_reward_threshold:
            create_reward = CampaignReward(campaign=campaign_selected, payment=payment, created_at=timezone.now(),
                                           rewarded_user_email=data['donatorEmail'],
                                           reward=campaign_selected.campaign_reward_details, reward_status="PENDING")
            create_reward.save()

    checkUser = AllSystemUser.objects.filter(email=data['donatorEmail']).exists()
    if checkUser is False:
        createUser = AllSystemUser(created_at=timezone.now(), username=data['donatorEmail'],
                                   email=data['donatorEmail'], user_type='Crowdfunder')
        createUser.save()

    responseData = {
        'message': 'Payment Received and Recorded'
    }
    return JsonResponse(responseData)




