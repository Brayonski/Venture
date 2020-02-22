# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from crowdfunding.models import *
from crowdfunding.tasks import *
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

# Register your models here.
class CampaignSectorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'added_by']
    #readonly_fields = ["added_by"]
    exclude = ['added_by']

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()


class CampaignConfigurationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'transaction_fee_type','transaction_fee','processing_fee_type','processing_fee','added_by']
    exclude = ['added_by']

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'sector', 'campaign_owner','target_amount','total_funds_received','duration','campaign_status')
    list_filter = ['created_at','sector','campaign_owner']
    search_fields = ['campaign_name']
    readonly_fields = ["campaign_status","created_at","total_funds_received","funds_disbursement_status","campaign_owner","approved_by","rejected_by"]
    exclude = ['approved','rejected']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved') is False and getattr(obj, 'rejected') is False:
            if form.cleaned_data['approval_status'] == "APPROVE":
                obj.approved = True
                obj.approved_by = request.user
                obj.campaign_status = 'APPROVED'
                obj.save()
                subject, from_email, to = 'Campaign Approval Request', settings.EMAIL_HOST_USER, obj.campaign_owner.email
                send_actioned_campaign_email_task.delay(obj.campaign_name, obj.id, subject, from_email, to, "approved")
            elif form.cleaned_data['approval_status'] == "REJECT":
                obj.rejected = True
                obj.rejected_by = request.user
                obj.campaign_status = 'REJECTED'
                obj.save()
                subject, from_email, to = 'Campaign Approval Request', settings.EMAIL_HOST_USER, obj.campaign_owner.email
                send_actioned_campaign_email_task.delay(obj.campaign_name, obj.id, subject, from_email, to, "rejected")


class CampaignPaymentAdmin(admin.ModelAdmin):
    search_fields = ['campaign__campaign_name']
    list_display = ['created_at','campaign', 'donator','amount','payment_method', 'payment_status']
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False


class CampaignDisbursementAdmin(admin.ModelAdmin):
    search_fields = ['campaign__campaign_name']
    list_display = ['created_at','campaign', 'amount', 'recipient', 'disbursement_type', 'disbursement_status']
    readonly_fields = ["campaign", "created_at", "campaign_target", "disbursement_status", "approved_by", "rejected_by", "campaign_duration"]
    exclude = ['approved', 'rejected']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved') is False and getattr(obj, 'rejected') is False:
            if form.cleaned_data['approval_status'] == "APPROVE":
                obj.approved = True
                obj.approved_by = request.user
                obj.disbursement_status = 'APPROVED'
                obj.campaign.funds_disbursement_status = 'APPROVED'
                obj.save()
                #handle disbursement task
                #if form.cleaned_data['disbursement_type'] == "DISBURSE":
                    #call disbursement method for funds to campiagn owner
                #else:
                    # call refunds method refunds to funders

            elif form.cleaned_data['approval_status'] == "REJECT":
                obj.rejected = True
                obj.rejected_by = request.user
                obj.disbursement_status = 'REJECTED'
                obj.campaign.funds_disbursement_status = 'REJECTED'
                obj.save()

class CampaignRewardAdmin(admin.ModelAdmin):
    search_fields = ['campaign__campaign_name']
    list_display = ['created_at','campaign', 'rewarded_user', 'reward', 'reward_status']
    readonly_fields = ["campaign", "rewarded_user", "reward", "created_at"]
    exclude = ['payment']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(CampaignSector, CampaignSectorAdmin)
admin.site.register(CampaignConfiguration, CampaignConfigurationAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignPayment, CampaignPaymentAdmin)
admin.site.register(CampaignDisbursement, CampaignDisbursementAdmin)
admin.site.register(CampaignReward, CampaignRewardAdmin)