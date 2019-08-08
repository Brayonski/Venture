# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import TextMedia, AudioVisual, Category, Subscription, Newsletter

class TextMediaAdmin(admin.ModelAdmin):
    list_filter = ['date', 'category', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'category', 'date']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        if getattr(obj, 'priority', None) is None:
            obj.priority = False
        obj.save()

class AudioVisualAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['date', 'category']
    readonly_fields = ["author"]
    list_display = ['title', 'date', 'category', 'sub_category']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        if getattr(obj, 'priority', None) is None:
            obj.priority = False
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ["author"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']
    list_filter = ['is_active']

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    readonly_fields = ["recipients"]

admin.site.register(TextMedia, TextMediaAdmin)
admin.site.register(AudioVisual, AudioVisualAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Newsletter, NewsletterAdmin)

