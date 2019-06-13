# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EventCategory, Events


class EventCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'author']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class EventsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category', 'author']
    list_filter = ['title', 'start_date', 'category', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'category', 'start_date', 'end_date', 'author']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Events, EventsAdmin)
