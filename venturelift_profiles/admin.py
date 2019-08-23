# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from venturelift_profiles.models import *
from venturelift_profiles.tasks import *
from django.conf import settings
from actstream.actions import follow, unfollow


class BusinessAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['size', 'sector', 'verified']
    list_display = ['name', 'sector', 'verified']
    readonly_fields = ["verified_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'verified_by', None) is None:
            obj.verified_by = request.user
        obj.save()


class SupporterAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username', 'verified']
    list_filter = ['verified']
    readonly_fields = ["verified_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'verified_by', None) is None:
            obj.verified_by = request.user
        obj.save()

    def username(self, obj):
        return obj.user.username


class SupporterProfileAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'company']
    search_fields = ['firstname', 'lastname']

    def firstname(self, obj):
        return obj.supporter_profile.user.first_name

    def lastname(self, obj):
        return obj.supporter_profile.user.last_name

    def company(self, obj):
        return obj.supporter_profile.company


class InvestorAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['get_username', 'verified']
    list_filter = ['verified']
    readonly_fields = ["verified_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'verified_by', None) is None:
            obj.verified_by = request.user
        obj.save()

    def get_username(self, obj):
        return obj.user.username


class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ['investor_profile']
    search_fields = ['investor_profile']

    def company_name(self, obj):
        return obj.investor_profile.company


class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ["added_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.save()


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'author', 'date']
    list_filter = ['date']

    def author(self, obj):
        if obj.supporter_author:
            return obj.supporter_author.user.username
        elif obj.investor_author:
            return obj.investor_author.user.username
        elif obj.company:
            return obj.company.name


class VlaServicesAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ["added_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.save()


class MarketDescriptionAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessModelAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessTeamAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessFinancialAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessInvestmentAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessGoalsAdmin(admin.ModelAdmin):
    list_display = ['company_name']
    search_fields = ['company_name']

    def company_name(self, obj):
        return obj.company_name.name


class BusinessConnectRequestAdmin(admin.ModelAdmin):
    search_fields = ['business__name']
    list_display = ['investor','business', 'created_at', 'approval_status']
    readonly_fields = ["investor", "business", "created_at"]
    exclude = ['approved_by','rejected_by','approved','rejected']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved') is False and getattr(obj, 'rejected') is False:
            if form.cleaned_data['approval_status'] == "APPROVE":
                obj.approved = True
                obj.approved_by = request.user
                obj.save()
                follow(obj.investor, obj.business)
            elif form.cleaned_data['approval_status'] == "REJECT":
                obj.rejected = True
                obj.rejected_by = request.user
                obj.save()
                subject, from_email, to = 'Business Connection Approval Notification', settings.EMAIL_HOST_USER, obj.investor.email
                send_investor_approved_connect_email_task.delay(obj.business.name, obj.investor.username,
                                                               subject, from_email, to)


class InvestorConnectRequestAdmin(admin.ModelAdmin):
    search_fields = ['investor__company']
    list_display = ['investor','requestor', 'created_at', 'approval_status']
    readonly_fields = ["investor", "requestor", "created_at"]
    exclude = ['approved_by','rejected_by','approved','rejected']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved') is False and getattr(obj, 'rejected') is False:
            if form.cleaned_data['approval_status'] == "APPROVE":
                obj.approved = True
                obj.approved_by = request.user
                obj.save()
                follow(obj.requestor, obj.investor)
            elif form.cleaned_data['approval_status'] == "REJECT":
                obj.rejected = True
                obj.rejected_by = request.user
                obj.save()
                subject, from_email, to = 'Investor Connection Approval Notification', settings.EMAIL_HOST_USER, obj.requestor.email
                send_investor_approved_connect_email_task.delay(obj.investor.company, obj.requestor.username,
                                                               subject, from_email, to)


class SupporterConnectRequestAdmin(admin.ModelAdmin):
    search_fields = ['supporter__company']
    list_display = ['supporter','requestor', 'created_at', 'approval_status']
    readonly_fields = ["supporter", "requestor", "created_at"]
    exclude = ['approved_by','rejected_by','approved','rejected']

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved') is False and getattr(obj, 'rejected') is False:
            if form.cleaned_data['approval_status'] == "APPROVE":
                obj.approved = True
                obj.approved_by = request.user
                obj.save()
                follow(obj.requestor, obj.supporter)
            elif form.cleaned_data['approval_status'] == "REJECT":
                obj.rejected = True
                obj.rejected_by = request.user
                obj.save()
                subject, from_email, to = 'Partner Connection Approval Notification', settings.EMAIL_HOST_USER, obj.requestor.email
                send_investor_approved_connect_email_task.delay(obj.supporter.company, obj.requestor.username,
                                                               subject, from_email, to)



class TrackingUserAdmin(admin.ModelAdmin):
    search_fields = ['user_details__email']
    list_display = ['user_details','user_email','action_name', 'access_time']
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False

class AllSystemUserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['created_at','username', 'email','user_type']
    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False


class SurveyUserAdmin(admin.ModelAdmin):
    search_fields = ['user__email']
    list_display = ['user','from_time','to_time']




admin.site.register(Business, BusinessAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Supporter, SupporterAdmin)
admin.site.register(SupporterProfile, SupporterProfileAdmin)
admin.site.register(BusinessCategory, BusinessCategoryAdmin)
admin.site.register(VlaServices, VlaServicesAdmin)
admin.site.register(MarketDescription, MarketDescriptionAdmin)
admin.site.register(BusinessModel, BusinessModelAdmin)
admin.site.register(BusinessTeam, BusinessTeamAdmin)
admin.site.register(BusinessFinancial, BusinessFinancialAdmin)
admin.site.register(BusinessInvestment, BusinessInvestmentAdmin)
admin.site.register(BusinessGoals, BusinessGoalsAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(InvestorProfile, InvestorProfileAdmin)
admin.site.register(BusinessConnectRequest, BusinessConnectRequestAdmin)
admin.site.register(InvestorConnectRequest, InvestorConnectRequestAdmin)
admin.site.register(SupporterConnectRequest, SupporterConnectRequestAdmin)
admin.site.register(TrackingUser, TrackingUserAdmin)
admin.site.register(AllSystemUser, AllSystemUserAdmin)
admin.site.register(SurveyUser, SurveyUserAdmin)
