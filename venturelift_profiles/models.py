# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from djangocms_text_ckeditor import fields
from django.core.validators import MinLengthValidator
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
from django.utils import timezone
# Create your models here.

BUSINESS_SIZE = (
    ('Startup', 'Startup: 2+ years post-revenue $10,000 p.a., 3+ full time teams'),
    ('SME', 'SME: 5+ years from first revenue, $500,000 p.a., 10+ full time team'),
)

SUPPORTER_INTEREST = (
    ('Professional Services', 'Professional Services'),
    ('Talent', 'Talent'),
    ('Technology', 'Technology'),
    ('Trade', 'Trade'),
    ('Supply Chain', 'Supply Chain'),
)

GENDER_TYPES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
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
)

INTEREST_STARTUPS = (
    ('SME', 'SME: 5+ years from first revenue, at least $500,000 in revenue in the last two years of operations, 10 + full time team'),
    ('Startup', 'Startup: 2+ years post-revenue, at least $100,000 in revenue in the last year of operations, 3+ full time team'),
)

INTEREST_SECTORS = (
    ('AGRIBUSINESS', 'AGRIBUSINESS'),
    ('CREATIVE', 'CREATIVE'),
    ('EDUCATION', 'EDUCATION'),
    ('FINANCIAL SERVICES', 'FINANCIAL SERVICES'),
    ('FMCG - RETAIL', 'FMCG - RETAIL'),
    ('HEALTH', 'HEALTH'),
    ('HOUSING & REAL ESTATE', 'HOUSING & REAL ESTATE'),
    ('RENEWABLE ENERGY', 'RENEWABLE ENERGY'),
    ('TECHNOLOGY', 'TECHNOLOGY'),
    ('WATER and SANITATION', 'WATER and SANITATION')
)
INVESTOR_FORMS = (
    ('equity', 'Equity'),
    ('debt', 'Debt'),
    ('mezzanine', 'Mezzanine'),
    ('grants', 'Grants'),
    ('crowdfunding platform', 'Crowdfunding Platform'),
)

INTEREST_COUNTRIES = (
('Top 15 Investment Countries',
    (
        ('Egypt', 'Egypt'),
        ('South Africa', 'South Africa'),
        ('Morocco', 'Morocco'),
        ('Ethiopia', 'Ethiopia'),
        ('Kenya', 'Kenya'),
        ('Rwanda', 'Rwanda'),
        ('Tanzania', 'Tanzania'),
        ('Nigeria', 'Nigeria'),
        ('Ghana', 'Ghana'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Algeria', 'Algeria'),
        ('Botswana', 'Botswana'),
        ('Zambia', 'Zambia'),
        ('tunisia', 'Tunisia'),
        ('Cote D` Ivore', 'Cote D` Ivore'),
    )
 ),
    ('Others',
      (
        ('Angola', 'Angola'),
        ('Benin', 'Benin'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cameroon', 'Cameroon'),
        ('Central African Republic (CAR)', 'Central African Republic (CAR)'),
        ('Chad', 'Chad'),
        ('Comoros', 'Comoros'),
        ('Djibouti', 'Djibouti'),
        ('DRC Congo', 'DRC Congo'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Guinea', 'Guinea'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Mali', 'Mali'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'),
        ('Niger', 'Niger'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Somalia', 'Somalia'),
        ('South Sudan', 'South Sudan'),
        ('Sudan', 'Sudan'),
        ('Togo', 'Togo'),
        ('Uganda', 'Uganda'),
        ('Zimbabwe', 'Zimbabwe'),
      )
   ),
)

TRADING_PARTNERS = (
    ('fair trade', 'Fair Trade'),
    ('haccp', 'HACCP'),
    ('ISO 9001', 'ISO 9001'),
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

BLOG_TYPES = (
    ('Corporate', 'Corporate'),
    ('Business Plans', 'Business Plans'),
    ('Financial Reports', 'Financial Reports'),
)

APPROVAL_STATUS = (
    ('APPROVE', 'APPROVE'),
    ('REJECT', 'REJECT'),
    ('PENDING', 'PENDING'),
)

FUNDER_TYPES = (
    ('Investor', 'Investor'),
    ('Crowdfunder', 'Crowdfunder'),
    ('Lender', 'Lender'),
    ('Grantor', 'Grantor'),
)

INVESTOR_TYPES = (
    ('Angel', 'Angel'),
    ('Venture Capital', 'Venture Capital'),
    ('Private Equity', 'Private Equity'),
    ('Impact', 'Impact'),
)

INVESTOR_PRODUCTS = (
    ('Equity', 'Equity'),
    ('Quasi Equity', 'Quasi Equity'),
    ('Other', 'Other'),
)

CROWDFUNDER_TYPES = (
    ('Donator', 'Donator'),
)

LENDER_PRODUCTS = (
    ('Subordinated', 'Subordinated'),
    ('Mezzanine', 'Mezzanine'),
    ('Senior', 'Senior'),
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
    gender = models.CharField(
        max_length=200, choices=GENDER_TYPES, default='Other')
    sector = models.ForeignKey(BusinessCategory)
    size = models.CharField(max_length=100, choices=BUSINESS_SIZE)
    creator = models.ForeignKey(User, related_name='business_creator')
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    company_primary_email = models.EmailField()
    company_website = models.CharField(max_length=200, null=True, blank=True)
    address = CountryField()
    year_of_company_registration = models.IntegerField(choices=YEAR_CHOICES)
    value_proposition_statement = models.TextField(null=True, blank=True)
    full_time_employee_count = models.IntegerField()
    verified = models.BooleanField(default=False)
    sample_profile = models.BooleanField(default=False)
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
    founders_info = models.TextField(null=True, blank=True)
    team_roles_and_structure = models.TextField(null=True, blank=True)
    board_of_advisors = models.TextField(null=True, blank=True)
    board_of_directors = models.TextField(null=True, blank=True)

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
    capital_to_raise = models.IntegerField(null=True, blank=True)

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
    gender = models.CharField(
        max_length=200, choices=GENDER_TYPES, default='Other')
    phone_number = models.CharField(max_length=20, validators=[
                                    MinLengthValidator(5)], help_text="My Phone Number", null=True)
    about = models.TextField(help_text="Briefly describe your self", null=True)
    company = models.CharField(max_length=250, unique=True, null=True)
    role = models.CharField(max_length=250, null=True)
    company_operations = CountryField(null=True)
    company_website = models.CharField(
        max_length=250, blank=True, null=True)
    company_registration_year = models.IntegerField(
        choices=YEAR_CHOICES, default=2010)
    verified = models.BooleanField(default=False)
    sample_profile = models.BooleanField(default=False)
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
        max_length=200, choices=SUPPORTER_INTEREST)

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


class Investor(models.Model):
    user = models.ForeignKey(User, related_name='investor_creator')
    about = models.TextField(null=True)
    thumbnail_image = models.ImageField(
        upload_to='pic_folder/', null=True, blank=True)
    gender = models.CharField(
        max_length=200, choices=GENDER_TYPES, default='Other')
    phone_number = models.CharField(max_length=20, validators=[
                                    MinLengthValidator(5)], help_text="My Phone Number")
    company = models.CharField(max_length=250)
    role = models.CharField(max_length=250)
    company_location = CountryField()
    physical_address = models.CharField(max_length=250)
    company_website = models.CharField(
        max_length=250, blank=True, null=True)
    company_registration_year = models.IntegerField(
        choices=YEAR_CHOICES)
    verified = models.BooleanField(default=False)
    sample_profile = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, related_name='investor_verifier', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name


class InvestorProfile(models.Model):
    investor_profile = models.ForeignKey(
        Investor, related_name='investor_profile')

    funder_type = models.CharField(max_length=255,null=True,choices=FUNDER_TYPES)
    investment_type = models.CharField(max_length=255,null=True,blank=True)
    investment_product = models.CharField(max_length=255,null=True,blank=True)
    # company_classification = models.CharField(
    #     max_length=50, choices=COMPANY_CLASSIFICATION, null=True, blank=True)

    # investor_forms = MultiSelectField(
    #     max_length=250, choices=INVESTOR_FORMS, null=True, blank=True, help_text="What forms of investment do you make?")

    target_sectors = models.ManyToManyField(BusinessCategory, help_text="Target Sectors", null=True, blank=True)

    target_countries = MultiSelectField(
        max_length=250, choices=INTEREST_COUNTRIES, help_text="Which are your target countries?", null=True, blank=True)

    elevator_pitch = models.TextField(help_text="What's your investment thesis in brief?", null=True)

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

    impact_metrics = models.TextField(help_text="Which are your key impact metrics", null=True)

    # gender_lens_investor = models.CharField(
    #     max_length=250, null=True, blank=True, choices=IMPACT_INVESTOR, help_text="Do you Consider your firm a 'Gender-Lens' Investor?",default='yes'
    # )

    class Meta:
        verbose_name = 'Investor Profile'
        verbose_name_plural = 'Investors Profiles'

    def __str__(self):
        return self.investor_profile.user.first_name + " " + self.investor_profile.user.last_name

class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    blog_type = models.CharField(max_length=100, choices=BLOG_TYPES, default="Corporate")
    company = models.ForeignKey(Business, null=True, blank=True, related_name="author_company")
    supporter_author = models.ForeignKey(
        Supporter, null=True, blank=True, related_name='author_supporter')
    investor_author = models.ForeignKey(
        Investor, null=True, blank=True, related_name='author_investor')
    file_name = models.FileField(
        upload_to='pic_folder/', null=True, blank=True, help_text="Upload an File")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    class Meta:
        verbose_name = 'Business Updates'
        verbose_name_plural = 'Business Updates'
        ordering = ('-date',)

    def __str__(self):
        return self.title

class BusinessConnectRequest(models.Model):
    business = models.ForeignKey(Business, related_name='business_to_follow')
    created_at = models.DateTimeField('request date',null=True)
    investor = models.ForeignKey(User, related_name='follow_requester')
    approval_status = models.CharField(
        max_length=100, choices=APPROVAL_STATUS, default="PENDING", null=True,blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='connection_approver', null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(User, related_name='conection_rejector', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Business Connect Request'

    def __str__(self):
        return self.business.name

class InvestorConnectRequest(models.Model):
    investor = models.ForeignKey(Investor, related_name='investor_to_follow')
    created_at = models.DateTimeField('request date',null=True)
    requestor = models.ForeignKey(User, related_name='investor_follow_requester')
    approval_status = models.CharField(max_length=100, choices=APPROVAL_STATUS, default="PENDING", null=True, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='investor_connection_approver', null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(User, related_name='investor_conection_rejector', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Investor Connect Request'

    def __str__(self):
        return self.investor.company



class SupporterConnectRequest(models.Model):
    supporter = models.ForeignKey(Supporter, related_name='supporter_to_follow')
    created_at = models.DateTimeField('request date',null=True)
    requestor = models.ForeignKey(User, related_name='supporter_follow_requester')
    approval_status = models.CharField(max_length=100, choices=APPROVAL_STATUS, default="PENDING", null=True, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, related_name='supporter_connection_approver', null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(User, related_name='supporter_conection_rejector', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Supporter Connect Request'

    def __str__(self):
        return self.supporter.company

class TrackingUser(models.Model):
    user_details = models.ForeignKey(User, related_name='logged_in_user')
    access_time = models.DateTimeField('system access date')
    action_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Tracking Logins'

    def __str__(self):
        return self.user_details.email

    def user_email(self):
        return self.user_details.email

class AllSystemUser(models.Model):
    created_at = models.DateTimeField('system access date', null=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'All System Users'

    def __str__(self):
        return self.email

    def user_email(self):
        return self.email


class SurveyUser(models.Model):
    user = models.ForeignKey(User)
    from_time = models.DateTimeField('allow system access from date')
    to_time = models.DateTimeField('allow system access to date')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Survey Users'

    def __str__(self):
        return self.user.email

    def user_email(self):
        return self.user.email