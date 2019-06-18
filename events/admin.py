# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EventCategory, Events, Attendees, NetworkEvents


class EventCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'author', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class EventAttendeesAdmin(admin.ModelAdmin):
    search_fields = ['event', 'attendee']
    list_filter = ['event', 'attendee', 'registration_date']
    list_display = ['event', 'attendee', 'registration_date']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'attendee', None) is None:
            obj.author = request.user
        obj.save()


class EventsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category', 'author']
    list_filter = ['title', 'start_date', 'category', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'category', 'start_date', 'end_date', 'author', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class NetworkEventsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category', 'organization_name']
    list_filter = ['title', 'start_date', 'category', 'organization_name']
    readonly_fields = ["author"]
    list_display = ['title', 'category',
                    'start_date', 'end_date', 'organization_name', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Attendees, EventAttendeesAdmin)
admin.site.register(NetworkEvents, NetworkEventsAdmin)
