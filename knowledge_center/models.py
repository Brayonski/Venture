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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document Category'
        verbose_name_plural = 'Document Categories'
		

class TextCenter(models.Model):
    category = models.ForeignKey(DocumentCategory, null=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    description = fields.HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENTSTATUS, default="")
    file_upload = models.FileField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Upload an File")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document/Article Manager'
        verbose_name_plural = 'Documents / Articles Manager'

class AudioVisual(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    author = models.ForeignKey(User, related_name="audiovisual_manager")
    category = models.CharField(max_length=100, choices=AUDIOVISUALCHOICES)
    sub_category = models.ForeignKey(DocumentCategory, null=True, help_text='Type of AUDIO VISUAL')
    payment_status = models.CharField(max_length=100, choices=PAYMENTSTATUS, default="free")
    description = fields.HTMLField(default="")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Audio/Visual Content Manager'
        verbose_name_plural = 'Audio/Visual Content Manager'