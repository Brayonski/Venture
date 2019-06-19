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

AUDIOVISUALCHOICES = (
    ("Podcast", "Podcast"),
    ("Video", "Video"),

)
PAYMENTSTATUS = (
    ("FREE", "free"),
    ("PREMIUM", "paid"),
)


class DocumentCategory(models.Model):
    """Document Category"""
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name="document_category_user")
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document Category'
        verbose_name_plural = 'Document Categories'


class VideoCategory(models.Model):
    """Video Category"""
    slug = models.SlugField(default="")
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, related_name="video_category_user")
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video Category'
        verbose_name_plural = 'Video Categories'


class TextCenter(models.Model):
    category = models.ForeignKey(DocumentCategory, null=True)
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    description = fields.HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=100, choices=PAYMENTSTATUS, default="", help_text="Payment Required", verbose_name='Payment Required?')
    file_upload = models.FileField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Upload an File")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document / Report Manager'
        verbose_name_plural = 'Documents / Reports Manager'


class AudioVisual(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    author = models.ForeignKey(User, related_name="videouser_manager")
    category = models.CharField(max_length=100, choices=AUDIOVISUALCHOICES)
    published = models.BooleanField(default=False)
    sub_category = models.ForeignKey(
        VideoCategory, null=True, help_text='Type of Video')
    payment_status = models.CharField(
        max_length=100, choices=PAYMENTSTATUS, default="free", help_text="Payment Required", verbose_name='Payment Required?')
    description = fields.HTMLField(default="")
    video_url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    #allowed_memberships = models.ManyToManyField(
    #    Membership, blank=True, null=True)
    youtube_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video Content Manager'
        verbose_name_plural = 'Video Content Manager'
