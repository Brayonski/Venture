# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from venturelift_profiles.models import Business, Supporter, BusinessCategory, Post

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
    list_display = ['get_username', 'verified']
    list_filter = ['verified']
    readonly_fields = ["verified_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'verified_by', None) is None:
            obj.verified_by = request.user
        obj.save()

    def get_username(self, obj):
        return obj.user.username

class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ["added_by"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.save()

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'get_username', 'date']
    list_filter = ['date']

    def get_username(self, obj):
        return obj.author.username

admin.site.register(Business, BusinessAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Supporter, SupporterAdmin)
admin.site.register(BusinessCategory, BusinessCategoryAdmin)