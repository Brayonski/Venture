# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields

# Create your models here.

BUSINESS_SIZE = (
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
)

class BusinessCategory(models.Model):
    name = models.CharField(max_length=100)
    added_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Business Categories'

class Business(models.Model):
    name = models.CharField(max_length=255)
    sector = models.ForeignKey(BusinessCategory)
    size = models.CharField(max_length=50, choices=BUSINESS_SIZE)
    creator = models.ForeignKey(User)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, related_name='business_verifier')

    class Meta:
        verbose_name_plural = 'Businesses'

    def __unicode__(self):
        return self.name

class Supporter(models.Model):
    user = models.ForeignKey(User)
    interests = models.ManyToManyField(BusinessCategory, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, related_name='supporter_verifier')

    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = fields.HTMLField()
    company = models.ForeignKey(Business, null=True, blank=True)
    author = models.ForeignKey(Supporter, null=True, blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title