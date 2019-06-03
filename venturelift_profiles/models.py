# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields
from django.core.validators import MinLengthValidator
from multiselectfield import MultiSelectField

# Create your models here.

BUSINESS_SIZE = (
    ('Startup', 'Startup: 2+ years post-revenue $10,000 p.a., 3+ full time teams'),
    ('SME', 'SME: 5+ years from first revenue, $500,000 p.a., 10+ full time team'),
)

SUPPORTER_INTEREST = (
    ('supply chain', 'Supply chain(i.e. I am looking for suppliers from Africa)'),
    ('trade partner', 'Trade partner: I want to trade with African companies'),
    ('technology provider', 'Technology Provider'),
    ('talent provider', 'Talent Provider'),
    ('professional support', 'Professional Support'),
)

COMPANY_CLASSIFICATION = (
    ('crowdfunder', 'Crowdfunder'),
    ('angel investor', 'Angel Investor'),
    ('venture capital', 'Venture Capital'),
    ('private equity', 'Private Equity'),
    ('fund of funds', 'Fund of Funds'),
    ('challenge funds', 'Challenge Fund'),
    ('commercial bank', 'Commercial Bank'),
    ('microfinance', 'Microfinance'),
    ('other', 'Other')
)

PROFESSIONAL_SUPPORT = (
    ('business accelerator', 'Business Accelerator'),
    ('business incubator', 'Business Incubator'),
    ('mentor', 'Mentor'),
    ('transaction advisor', 'Transaction Advisor'),
    ('accounting and finance', 'Accounting And Finance'),
    ('legal', 'Legal'),
    ('technology', 'Technology')
)

INTEREST_STARTUPS = (
    ('SME', 'SME: 5+ years from first revenue, at least $500,000 in revenue in the last two years of operations, 10 + full time team'),
    ('Startup', 'Startup: 2+ years post-revenue, at least $100,000 in revenue in the last year of operations, 3+ full time team'),
    ('both', 'Both SMEs and Startups')
)

INTEREST_SECTORS = (
    ('retail', 'Retail'),
    ('fmcg', 'FMCG'),
    ('technology', 'Technology'),
    ('manufacturing', 'Manufacturing'),
    ('agriculture', 'Agriculture'),
    ('hospitality', 'Hospitality and Tourism'),
    ('real estate', 'Real Estate and Infastructure'),
    ('transport', 'Transport')
)
INVESTOR_FORMS = (
    ('equity', 'Equity'),
    ('debt', 'Debt'),
    ('mezzanine', 'Mezzanine'),
    ('grants', 'Grants'),
    ('crowdfunding platform', 'Crowdfunding Platform'),
    ('other', 'Other')
)

INTEREST_COUNTRIES = (
    ('rwanda', 'Rwanda'),
    ('uganda', 'Uganda'),
    ('tanzania', 'Tanzania'),
    ('kenya', 'Kenya'),
    ('ghana', 'Ghana'),
    ('nigeria', 'Nigeria'),
    ('ivory coast', 'Ivory Coast'),
    ('senegal', 'Senegal'),
    ('botswana', 'Bootswana'),
    ('nambia', 'Nambia'),
    ('zambia', 'Zambia'),
    ('south africa', 'South Africa'),
    ('egypt', 'Egypt'),
    ('tunisia', 'Tunisia'),
    ('morocco', 'Morocco'),
    ('other eastern africa ', 'Other Eastern Africa'),
    ('other western africa', 'Other Western Africa'),
    ('other northern africa', 'Other Nothern Africa'),
    ('other francophone africa', 'Other Francophone africa'),
    ('other southern africa', 'Other Southern Africa'),
    ('other', 'Other'),
)

TRADING_PARTNERS = (
    ('fair trade', 'Fair Trade'),
    ('haccp', 'HACCP'),
    ('ISO 9001', 'ISO 9001'),
    ('other', 'Other'),
)

MANAGED_FUNDS = (
    ('1', '1'),
    ('1-5', '1-5'),
    ('5+', '5+')
)

AUM = (
    ('<usd 1M', '<USD 1M'),
    ('usd 1 - 10', 'USD 1M - USD 10M'),
    ('usd 10 - 50', 'USD 10M - USD 50M'),
    ('usd 50 - 100', 'USD 5M - USD 100M'),
    ('usd 100 - 250', 'USD 100M - USD 250M'),
    ('usd 250 - 500', 'USD 250M - USD 500M'),
    ('usd 500 - 1b', 'USD 500M - USD 1B'),
    ('over 1b', 'OVER USD 1B')
)

INVESTOR_PORTFOLIO = (
    ('< 5', '<5'),
    ('5-10', '5 - 10'),
    ('10-20', '10 - 20'),
    ('over 20', 'Over 20'),
)
EXIT_EXECUTED = (
    ('none', 'NONE'),
    ('< 5', '< 5'),
    ('5-10', '5 - 10'),
    ('10-20', '10 - 20'),
    ('Over 20', 'Over 20')
)

IMPACT_INVESTOR = (
    ('yes', 'YES'),
    ('no', 'NO'),
    ('maybe', 'Maybe')
)

IMPACT_MEASUREMENT = (
    ('giin iris', 'GIIN IRIS'),
    ('b-corp', 'B-Corp'),
    ('msci', 'MSCI Sustainable Impact Metrics'),
    ('proprietary standard', 'Proprietary Standard'),
    ('other', 'other')
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
    size = models.CharField(max_length=100, choices=BUSINESS_SIZE)
    creator = models.ForeignKey(User, related_name='business_creator')
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    company_primary_email = models.EmailField()
    company_secondary_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(max_length=200, null=True, blank=True)
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
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, validators=[
                                    MinLengthValidator(5)], help_text="My Phone Number", null=True)
    about = models.CharField(
        max_length=250, help_text="Briefly describe your self?", null=True)
    company = models.CharField(max_length=250, unique=True, null=True)
    role = models.CharField(max_length=250, null=True)
    company_operations = models.CharField(max_length=250, null=True)
    physical_address = models.CharField(max_length=250, null=True)
    postal_address = models.CharField(max_length=250, null=True)
    company_website = models.URLField(
        max_length=250, blank=True, null=True)
    company_registration_year = models.IntegerField(
        choices=YEAR_CHOICES, default=2010)
    year_operation = models.IntegerField(choices=YEAR_CHOICES, default=2010)
    facebook_profile = models.URLField(
        max_length=200, null=True, blank=True, help_text="https://www.facebook.com/my user name")
    linkedin_profile = models.URLField(
        max_length=200, null=True, blank=True, help_text="https://www.linkedin.com/in/my user name")
    twitter_profile = models.URLField(
        max_length=200, null=True, blank=True, help_text="https://twitter.com/my user name")
    instagram_profile = models.URLField(
        max_length=200, null=True, blank=True, help_text="https://www.instagram.com/my user nam ")
    subscribe = models.BooleanField(default=True)
    interests = models.ManyToManyField(BusinessCategory, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, related_name='supporter_verifier', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name


class SupporterProfile(models.Model):
    supporter_profile = models.ForeignKey(
        Supporter, related_name='supporter_profile')
    supporter_interest = models.CharField(
        max_length=50, choices=SUPPORTER_INTEREST)

    professional_support = models.CharField(
        max_length=50, choices=PROFESSIONAL_SUPPORT, null=True, blank=True)

    interest_startups = models.CharField(
        max_length=50, choices=INTEREST_STARTUPS, null=True, blank=True)

    interest_sectors = models.ManyToManyField(BusinessCategory, help_text="Target Sectors", null=True, blank=True)

    interest_countries = MultiSelectField(
        max_length=250, choices=INTEREST_COUNTRIES, null=True, blank=True, help_text="Counties of Interest")

    trading_partners = MultiSelectField(
        max_length=50, choices=TRADING_PARTNERS, null=True, blank=True)

    class Meta:
        verbose_name = 'Supporter Profile'
        verbose_name_plural = 'Supporters Profiles'

    def __str__(self):
        return self.supporter_profile.user.first_name + " " + self.supporter_profile.user.last_name

    def verification_status(self):
        count = 0
        if not (self.supporter_profile.instagram_profile):
            count -= 1
        else:
            count += 1
        if not (self.supporter_profile.facebook_profile):
            count -= 1
        else:
            count += 1

        if not (self.supporter_profile.linkedin_profile):
            count -= 1
        else:
            count += 1

        if not (self.supporter_profile.twitter_profile):
            count -= 1
        else:
            count += 1

        if not (self.supporter_profile.company_website):
            count -= 1
        else:
            count += 1

        if not (self.supporter_profile.thumbnail_image):
            count -= 1
        else:
            count += 1

        if not (self.supporter_interest):
            count -= 1
        else:
            count += 1

        if not (self.professional_support):
            count -= 1
        else:
            count += 1

        if not (self.interest_startups):
            count -= 1
        else:
            count += 1

        if not (self.interest_sectors):
            count -= 1
        else:
            count += 1

        if not (self.interest_countries):
            count -= 1
        else:
            count += 1

        if not (self.trading_partners):
            count -= 1
        else:
            count += 1

        if count == 0:
            return 100
        elif count < 0:
            return 0
        else:
            return round((count/12)*100)


class Investor(models.Model):
    user = models.ForeignKey(User, related_name='investor_creator')
    about = models.CharField(
        max_length=250, help_text="Briefly describe your self?", null=True)
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, validators=[
                                    MinLengthValidator(5)], help_text="My Phone Number")
    company = models.CharField(max_length=250)
    role = models.CharField(max_length=250)
    company_location = models.CharField(max_length=250)
    physical_address = models.CharField(max_length=250)
    company_website = models.URLField(
        max_length=250, blank=True, null=True)
    company_registration_year = models.IntegerField(
        choices=YEAR_CHOICES)
    year_operation = models.IntegerField(choices=YEAR_CHOICES)
    facebook_profile = models.URLField(max_length=200, null=True, blank=True)
    linkedin_profile = models.URLField(max_length=200, null=True, blank=True)
    twitter_profile = models.URLField(max_length=200, null=True, blank=True)
    instagram_profile = models.URLField(max_length=200, null=True, blank=True)
    subscribe = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, related_name='investor_verifier', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name


class InvestorProfile(models.Model):
    investor_profile = models.ForeignKey(
        Investor, related_name='investor_profile')

    company_classification = models.CharField(
        max_length=50, choices=COMPANY_CLASSIFICATION, null=True, blank=True, help_text="How would you classify your firm?")

    investor_forms = MultiSelectField(
        max_length=250, choices=INVESTOR_FORMS, null=True, blank=True, help_text="What forms of investment do you make?")

    target_sectors = models.ManyToManyField(BusinessCategory, help_text="Target Sectors", null=True, blank=True)

    target_countries = MultiSelectField(
        max_length=250, choices=INTEREST_COUNTRIES, help_text="Which are your target countries?", null=True, blank=True)

    elevator_pitch = fields.HTMLField(
        null=True, blank=True, help_text="What's your investment thesis in brief?")

    managed_funds = models.CharField(
        max_length=100, null=True, blank=True, choices=MANAGED_FUNDS, help_text="How Many different funds have you managed to date?")

    assets_under_management = models.CharField(
        max_length=250, null=True, blank=True, choices=AUM, help_text="What's the value of your Assets under Management (AUM)?")

    investor_portfolio = models.CharField(
        max_length=250, null=True, blank=True, choices=INVESTOR_PORTFOLIO, help_text="How many active portfolio investments do you currently hold?")

    exits_executed = models.CharField(
        max_length=250, null=True, blank=True, choices=EXIT_EXECUTED, help_text="How many exits have you executed to date?")

    impact_investor = models.CharField(
        max_length=250, null=True, blank=True, choices=IMPACT_INVESTOR, help_text="Do you classify yourself as an impact investor?")

    impact_measurement = models.CharField(
        max_length=250, null=True, blank=True, choices=IMPACT_MEASUREMENT, help_text="Which impact measurement standard do you follow?")

    impact_metrics = fields.HTMLField(
        max_length=250, null=True, blank=True, help_text="Which are your key impact metrics")

    gender_lens_investor = models.CharField(
        max_length=250, null=True, blank=True, choices=IMPACT_INVESTOR, help_text="Do you Consider your firm a 'Gender-Lens' Investor?"
    )

    class Meta:
        verbose_name = 'Investor Profile'
        verbose_name_plural = 'Investors Profiles'

    def __str__(self):
        return self.investor_profile.user.first_name + " " + self.investor_profile.user.last_name

    def verification_status(self):
        count = 0
        if not (self.investor_profile.facebook_profile):
            count -= 1
        else:
            count += 1

        if not (self.investor_profile.thumbnail_image):
            count -= 1
        else:
            count += 1

        if not (self.investor_profile.company_website):
            count -= 1
        else:
            count += 1

        if not (self.investor_profile.linkedin_profile):
            count -= 1
        else:
            count += 1

        if not (self.investor_profile.twitter_profile):
            count -= 1
        else:
            count += 1

        if not (self.investor_profile.instagram_profile):
            count -= 1
        else:
            count += 1

        if not (self.company_classification):
            count -= 1
        else:
            count += 1

        if not (self.investor_forms):
            count -= 1
        else:
            count += 1

        if not (self.target_sectors):
            count -= 1
        else:
            count += 1

        if not (self.target_countries):
            count -= 1
        else:
            count += 1

        if not (self.elevator_pitch):
            count -= 1
        else:
            count += 1

        if not (self.managed_funds):
            count -= 1
        else:
            count += 1

        if not (self.assets_under_management):
            count -= 1
        else:
            count += 1

        if not (self.investor_portfolio):
            count -= 1
        else:
            count += 1

        if not (self.exits_executed):
            count -= 1
        else:
            count += 1

        if not (self.impact_investor):
            count -= 1
        else:
            count += 1

        if not (self.impact_measurement):
            count -= 1
        else:
            count += 1

        if not (self.impact_metrics):
            count -= 1
        else:
            count += 1

        if not (self.gender_lens_investor):
            count -= 1
        else:
            count += 1

        if count == 0:
            return 100
        elif count < 0:
            return 0
        else:
            return (round((count/14)*100))


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = fields.HTMLField()
    company = models.ForeignKey(Business, null=True, blank=True)
    supporter_author = models.ForeignKey(
        Supporter, null=True, blank=True, related_name='author_supporter')
    investor_author = models.ForeignKey(
        Investor, null=True, blank=True, related_name='author_investor')
    post_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Upload an Image")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    class Meta:
        verbose_name = 'Business Updates'
        verbose_name_plural = 'Business Updates'
        ordering = ('-date',)

    def __str__(self):
        return self.title
