# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Campaign, CampaignSector
from venturelift_profiles.models import Business
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

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


@login_required
def business_campaign_view(request, campaign_id):
    campaign = Campaign.objects.filter(id=campaign_id)
    campaign_sectors = CampaignSector.objects.all()
    template = loader.get_template('crowdfunding/investor/index.html')

    context = {
        'campaign_list': campaign,
        'campaign_sectors': campaign_sectors
    }
    return HttpResponse(template.render(context, request))


@login_required
def create_campaign(request):
    campaign_sectors = CampaignSector.objects.all()
    business = Business.objects.get(creator=request.user)
    template = loader.get_template('crowdfunding/business/create_campaign.html')

    context = {
        'campaign_sectors': campaign_sectors,
        'business': business
    }
    return HttpResponse(template.render(context, request))


