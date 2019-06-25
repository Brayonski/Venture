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
        raise errors


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


def get_online_checkout_response(request):
    response = '{"success":"true","message":"Received"}'
    return HttpResponse(response)





@login_required
def make_payment(request):
    if request.user.is_authenticated() and not (request.user.business_creator.exists()) and not (
            request.user.supporter_creator.exists()) and not (request.user.investor_creator.exists()):
        return redirect(reverse('profile_create'))
    campaign_selected = Campaign.objects.get(id=request.POST['campaign_id'])
    payment = CampaignPayment(campaign=campaign_selected,created_at=timezone.now(),donator=request.user,donator_email=request.user.email,donator_phoneno=request.POST['donator_phoneno'],amount=request.POST['amount'],payment_method=request.POST['payment_method'],payment_status='INITIATED',paid=False,comments=request.POST['comments'],allow_visibility=request.POST['allow_visibility'])
    payment.save()
    if campaign_selected.campaign_type == "REWARD BASED":
        if request.POST['amount'] >= campaign_selected.campaign_reward_threshold:
            create_reward = CampaignReward(campaign=campaign_selected,payment=payment,created_at=timezone.now(),rewarded_user=request.user,rewarded_user_email=request.user.email,reward=campaign_selected.campaign_reward_details,reward_status="PENDING")
            create_reward.save()
    template = loader.get_template('crowdfunding/investor/index.html')
    campaign_data = Campaign.objects.filter(campaign_status='APPROVED')
    campaign_sectors = CampaignSector.objects.all()

    context = {
        'campaign_list': campaign_data,
        'campaign_sectors': campaign_sectors,
        'message': 'Payment Initiated For Campaign '+campaign_selected.campaign_name+'. Please Check Your Phone For The STK-Push'
    }
    send_mpesa_stk_task.delay(request.POST['donator_phoneno'],request.POST['amount'])
    return HttpResponse(template.render(context, request))


def crowdfunder_make_payment(request):
    campaign_selected = Campaign.objects.get(id=request.POST['campaign_id'])
    payment = CampaignPayment(campaign=campaign_selected,created_at=timezone.now(),donator_email=request.POST['donator_email'],donator_phoneno=request.POST['donator_phoneno'],amount=request.POST['amount'],payment_method=request.POST['payment_method'],payment_status='INITIATED',paid=False,comments=request.POST['comments'],allow_visibility=request.POST['allow_visibility'])
    payment.save()
    if campaign_selected.campaign_type == "REWARD BASED":
        if request.POST['amount'] >= campaign_selected.campaign_reward_threshold:
            create_reward = CampaignReward(campaign=campaign_selected,payment=payment,created_at=timezone.now(),rewarded_user_email=request.POST['donator_email'],reward=campaign_selected.campaign_reward_details,reward_status="PENDING")
            create_reward.save()
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
    #send_mpesa_stk_task.delay(request.POST['donator_phoneno'],request.POST['amount'])
    try:
        get_mpesa_token(request.POST['donator_phoneno'],request.POST['amount'])
    except:
        print("There is an issue")
    return HttpResponse(template.render(context, request))


def get_mpesa_token(phone,amount):
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y%m%d%H%M%S")
    template = loader.get_template('crowdfunding/investor/mpesa.html')
    consumer_key = "G4fR8iS27KSOwAJ5eOtRq0MFdwDVbwau"
    consumer_secret = "BrPh8l8ZbpCQAoUt"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    responseToken = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    responseTokenData = json.loads(responseToken.text)
    accessToken = responseTokenData["access_token"]
    shortCode = "174379"
    passKey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    passwordMpesa = shortCode+passKey+formatedDate
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
            "Amount": amount,
            "PartyA": phone,
            "PartyB": shortCode,
            "PhoneNumber": phone,
            "CallBackURL": "http://http://52.37.84.193:8081/crowdfunding/mpesa_checkout_response",
            "AccountReference": "ACCOUNT01",
            "TransactionDesc": "VENTURELIFTDONATION"
        }

        response = requests.post(api_url, json=request, headers=headers)
        checkoutResponse = json.dumps(response.text)

    # context = {
    #     'tokendata': checkoutResponse,
    # }
    # return HttpResponse(template.render(context, request))
    return "STK SENT"

