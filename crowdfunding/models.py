# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import date

# Create your models here.

FEE_TYPE = (
    ('Percentage', 'Percentage'),
    ('Flat', 'Flat'),
)

APPROVAL_STATUS = (
    ('APPROVE', 'APPROVE'),
    ('REJECT', 'REJECT'),
    ('PENDING', 'PENDING'),
)

DISBURSEMENT_TYPE = (
    ('DISBURSE', 'DISBURSE'),
    ('REFUND', 'REFUND'),
)

class CampaignSector(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Campaign Sectors'


class CampaignConfiguration(models.Model):
    name = models.CharField(max_length=255)
    transaction_fee_type = models.CharField(max_length=100, choices=FEE_TYPE)
    transaction_fee = models.DecimalField(max_digits=19, decimal_places=2)
    processing_fee_type = models.CharField(max_length=100, choices=FEE_TYPE)
    processing_fee = models.DecimalField(max_digits=19, decimal_places=2)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Campaign Configurations'



class Campaign(models.Model):
    campaign_name = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created')
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField()
    sector = models.ForeignKey(CampaignSector)
    duration = models.DateField('campaign closing date')
    target_amount = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(10)])
    total_funds_received = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    campaign_status = models.CharField(max_length=100)
    campaign_owner = models.ForeignKey(User, related_name='campaign_business_owner')
    campaign_image = models.ImageField(upload_to='pic_folder/', null=True, blank=True, help_text="Upload a Campaign Image")
    short_description = models.TextField()
    long_description = models.TextField(null=True, blank=True)
    funds_disbursement_status = models.CharField(max_length=100)
    approval_status = models.CharField(max_length=100, choices=APPROVAL_STATUS, default="PENDING", null=True, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='campaign_approver', null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(User, related_name='campaign_rejector', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Campaigns'

    def __str__(self):
        return self.campaign_name

    def clean(self):
        if self.target_amount < 10:
            raise ValidationError(_('Only amounts equal to 10 or greater are accepted.'))


class CampaignPayment(models.Model):
    campaign = models.ForeignKey(Campaign)
    created_at = models.DateTimeField('donation date',null=True)
    donator = models.ForeignKey(User, related_name='campaign_donator')
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_order_number = models.CharField(max_length=255,null=True,blank=True)
    paid = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Campaign Payments'

    def __str__(self):
        return self.payment_order_number


class CampaignDisbursement(models.Model):
    campaign = models.ForeignKey(Campaign)
    created_at = models.DateTimeField('donation date', null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    disbursement_type = models.CharField(max_length=100, choices=DISBURSEMENT_TYPE, null=True, blank=True)
    disbursement_method = models.CharField(max_length=100, null=True, blank=True)
    disbursement_status = models.CharField(max_length=100)
    recipient = models.ForeignKey(User, related_name='disbursement_recipient')
    recipient_email = models.CharField(max_length=255, null=True, blank=True)
    approval_status = models.CharField(max_length=100, choices=APPROVAL_STATUS, default="PENDING", null=True,
                                       blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='disbursement_approver', null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(User, related_name='disbursement_rejector', null=True, blank=True)
    disbursement_order_number = models.CharField(max_length=255, null=True, blank=True)
    disbursed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Campaign Disbursements'

    def __str__(self):
        return self.campaign.campaign_name