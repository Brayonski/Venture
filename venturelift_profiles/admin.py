# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from venturelift_profiles.models import *


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
        return obj.author.user.username


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
