# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields

# Create your models here.

BUSINESS_SIZE = (
    ('Startup', 'Startup: 2+ years post-revenue $10,000 p.a., 3+ full time teams'),
    ('SME', 'SME: 5+ years from first revenue, $500,000 p.a., 10+ full time team'),
)

FUNDING_SOURCES = (
    ('bootstrap/own funds', 'bootstrap/own funds'),
    ('business revenue', 'business revenue'),
    ('personal loans', 'personal loans'),
)

YEAR_CHOICES = []
for r in range(1960, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


class BusinessCategory(models.Model):
    name = models.CharField(max_length=100)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Business Categories'


class VlaServices(models.Model):
    name = models.CharField(max_length=250)
    added_by = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = 'Vla Services'

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=255)
    sector = models.ForeignKey(BusinessCategory)
    size = models.CharField(max_length=50, choices=BUSINESS_SIZE)
    creator = models.ForeignKey(User, related_name='business_creator')
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    company_primary_email = models.EmailField()
    company_secondary_email = models.EmailField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=200, null=True, blank=True)
    linkedin_profile = models.URLField(max_length=200, null=True, blank=True)
    twitter_profile = models.URLField(max_length=200, null=True, blank=True)
    instagram_profile = models.URLField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    year_of_company_registration = models.IntegerField(choices=YEAR_CHOICES)
    value_proposition_statement = models.TextField(null=True, blank=True)
    full_time_employee_count = models.IntegerField()
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, related_name='business_verifier', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name


class MarketDescription(models.Model):
    company_name = models.ForeignKey(Business)
    product_offering = models.TextField(null=True, blank=True)
    market_segment = models.TextField(null=True, blank=True)
    needs_fulfilled_by_product = models.TextField(null=True, blank=True)
    market_size = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Business Market Description'
        verbose_name_plural = 'Business Market Description'

    def __str__(self):
        return self.company_name.name


class BusinessModel(models.Model):
    company_name = models.ForeignKey(Business)
    business_model = models.TextField(null=True, blank=True)
    competitors = models.TextField(null=True, blank=True)
    competitive_advantage = models.TextField(null=True, blank=True)
    intellectual_property_info = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Business Model'
        verbose_name_plural = 'Business Models'

    def __str__(self):
        return self.company_name.name


class BusinessTeam(models.Model):
    company_name = models.ForeignKey(Business)
    founders_info = models.FileField(
        upload_to='founders_info/', null=True, blank=True)
    team_roles_and_structure = models.FileField(
        upload_to='team_info/', null=True, blank=True)
    number_of_staff = models.IntegerField(null=True, blank=True)
    board_of_advisors = models.FileField(
        upload_to='board_advisors/', null=True, blank=True)
    board_of_directors = models.FileField(
        upload_to='board_directors/', null=True, blank=True)

    class Meta:
        verbose_name = 'Business Team'
        verbose_name_plural = 'Business Teams'

    def __str__(self):
        return self.company_name.name


class BusinessFinancial(models.Model):
    company_name = models.ForeignKey(Business)
    last_year_revenue = models.IntegerField(null=True, blank=True)
    last_year_profit = models.IntegerField(null=True, blank=True)
    growth_margin = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Business Financials'
        verbose_name_plural = 'Business Financials'

    def __str__(self):
        return self.company_name.name


class BusinessInvestment(models.Model):
    company_name = models.ForeignKey(Business)
    funding_source = models.CharField(
        max_length=200, choices=FUNDING_SOURCES, null=True, blank=True)
    personal_funds_invested = models.IntegerField(null=True, blank=True)
    external_funds_invested = models.IntegerField(null=True, blank=True)
    current_debt = models.BooleanField(default=False)
    capital_to_raise = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Business Investment'
        verbose_name_plural = 'Business Investments'

    def __str__(self):
        return self.company_name.name


class BusinessGoals(models.Model):
    company_name = models.ForeignKey(Business, related_name='business_goals')
    three_year_targeted_revenue = models.TextField(null=True, blank=True)
    constraints_to_growth = models.TextField(null=True, blank=True)
    primary_services_interested_in = models.ManyToManyField(
        VlaServices, blank=True, related_name='primary_services')
    secondary_services_interested_in = models.ManyToManyField(
        VlaServices, blank=True, related_name='secondary_services')

    class Meta:
        verbose_name = 'Business Goal'
        verbose_name_plural = 'Business Goals'

    def __str__(self):
        return self.company_name.name


class Supporter(models.Model):
    user = models.ForeignKey(User, related_name='supporter_creator')
    interests = models.ManyToManyField(BusinessCategory, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, related_name='supporter_verifier', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = fields.HTMLField()
    company = models.ForeignKey(Business, null=True, blank=True)
    author = models.ForeignKey(
        Supporter, null=True, blank=True, related_name='author')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    class Meta:
        verbose_name = 'Business Updates'
        verbose_name_plural = 'Business Updates'
        ordering = ('-date',)

    def __str__(self):
        return self.title
