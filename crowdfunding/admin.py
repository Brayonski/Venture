# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from crowdfunding.models import *

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



class CampaignApprovalAdmin(admin.ModelAdmin):
    search_fields = ['campaign']
    list_filter = ['campaign']
    list_display = ['campaign_creation_date', 'campaign_nam', 'campaign_sector', 'target_am','status']
    readonly_fields = ["approved_by","rejected_by"]

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(CampaignSector, CampaignSectorAdmin)
admin.site.register(CampaignConfiguration, CampaignConfigurationAdmin)
admin.site.register(CampaignApproval, CampaignApprovalAdmin)