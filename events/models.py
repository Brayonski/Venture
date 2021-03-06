# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields
from filer.fields.image import FilerImageField
from newsletter_subscription.models import SubscriptionBase
from django.conf import settings
from venturelift_cms.tasks import send_notification

REGISTRATION = (
    ("NO", "NO"),
    ("YES", "YES"),
)


class EventCategory(models.Model):
    """Event Category"""
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name="event_category_author")
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event Category'
        verbose_name_plural = 'Event Categories'


class Events(models.Model):
    category = models.ForeignKey(EventCategory, null=True)
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    description = fields.HTMLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    registration_url = models.CharField(max_length=50, null=True, blank=True)
    registration_required = models.CharField(
        max_length=100, choices=REGISTRATION)
    event_banner = models.FileField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Event Banners")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'VLA Events Manager'
        verbose_name_plural = 'VLA Events Manager'


class NetworkEvents(models.Model):
    category = models.ForeignKey(
        EventCategory, null=True, related_name="network_events")
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    organization_name = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    description = fields.HTMLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    registration_url = models.URLField(
        max_length=250, null=True, blank=True)
    registration_required = models.CharField(
        max_length=100, choices=REGISTRATION)
    event_banner = models.FileField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Event Banners")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Network Events Manager'
        verbose_name_plural = 'Network Events Manager'


class Attendees(models.Model):
    event = models.ForeignKey(Events, related_name="event_attendee")
    attendee = models.ForeignKey(User)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title

    class Meta:
        verbose_name = 'Event Attendees'
        verbose_name_plural = 'Event Attendees'
