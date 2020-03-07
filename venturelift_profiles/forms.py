from venturelift_profiles.models import *
from django.forms import ModelForm
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_countries.widgets import CountrySelectWidget

class CreateBusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['verified', 'verified_by', 'creator']
        widgets = {'address': CountrySelectWidget()}
        labels = {
            "thumbnail_image": "Company logo",
            "name": "Company name",
            "about": "about",
            "gender": "Gender",
            "sector": "Industry",
            "size": "Company size",
            "company_primary_email": "Company primary email address",
            "year_of_company_registration": "Year of Company Registration",
            "full_time_employee_count": "Number of full time employees",
            "address": "Country",
            "value_proposition_statement": "Value Proposition Statement",
        }
class CreateBlogForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['date', 'likes', 'supporter_author', 'investor_author', "company"]

        labels = {
            "blog_type": "Document Type",
            "file_name": "PDF Document to share",
            "title": "Subject",
            "body": "Description",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateBlogForm, self).__init__(*args, **kwargs)

class MarketDescriptionForm(ModelForm):
    class Meta:
        model = MarketDescription
        exclude = ['company_name']

        labels = {
            "product_offering": "Product/Service offered",
            "market_segment": "Market Segment",
            "needs_fulfilled_by_product": "Needs fulfilled by Product/Service",
            "market_size": "Market Size",
        }

class BusinessModelForm(ModelForm):
    class Meta:
        model = BusinessModel
        exclude = ['company_name']


class BusinessTeamForm(ModelForm):
    class Meta:
        model = BusinessTeam
        exclude = ['company_name']

        labels = {
            "board_of_advisors": "Board of advisors information",
            "board_of_directors": "Board of directors information",
        }

class BusinessFinancialForm(ModelForm):
    class Meta:
        model = BusinessFinancial
        exclude = ['company_name']


class BusinessInvestmentForm(ModelForm):
    class Meta:
        model = BusinessInvestment
        exclude = ['company_name']


class BusinessGoalsForm(ModelForm):
    class Meta:
        model = BusinessGoals
        exclude = ['company_name']

    primary_services_interested_in = forms.ModelMultipleChoiceField(queryset=VlaServices.objects.all(),
                                                                    widget=Select2MultipleWidget,required=False)

    secondary_services_interested_in = forms.ModelMultipleChoiceField(queryset=VlaServices.objects.all(),
                                                                    widget=Select2MultipleWidget,required=False)


COMPANY_SIZE = (
    ('', ''),
    ('Startup', 'Startup: 2+ years post-revenue $10,000 p.a., 3+ full time teams'),
    ('SME', 'SME: 5+ years from first revenue, $500,000 p.a., 10+ full time team'),
)

PROFILE_CHOICES = (
    ('Business', 'BUSINESS'),
    ('Investor', 'INVESTOR'),
    ('Supporter', 'SUPPORTER')
)

IMPACT_INVESTOR = (
    ('yes', 'YES'),
    ('no', 'NO'),
    ('maybe', 'Maybe')
)

FUNDER_TYPES = (
    ('Investor', 'Investor'),
    ('Crowdfunder', 'Crowdfunder'),
    ('Lender', 'Lender'),
    ('Grantor', 'Grantor'),
)

AVERAGE_PAYBACK = (
    ('1 month', '1 month'),
    ('2-3 months', '2-3 months'),
    ('6-12 months', '6-12 months'),
)



class BusinessFilters(forms.Form):
    service = forms.ModelChoiceField(queryset=VlaServices.objects.all(), required=False,
                                     label='Resources needed')
    sector = forms.ModelChoiceField(queryset=BusinessCategory.objects.all().order_by('name'), required=False,
                                    label='Sector')

    size = forms.ChoiceField(label='Company Stage',
                             choices=COMPANY_SIZE, required=False)


class SupporterFilters(forms.Form):
    size = forms.ChoiceField(
        widget=Select2Widget, label='Company Stage interested in', choices=INTEREST_STARTUPS, required=False)
    countries = forms.MultipleChoiceField(widget=Select2MultipleWidget,
                                          label='Countries of interest', required=False,
                                          choices=INTEREST_COUNTRIES)


class InvestorFilters(forms.Form):
    sectors = forms.ModelMultipleChoiceField(queryset=BusinessCategory.objects.all(), widget=Select2MultipleWidget,required=False)
    countries = forms.MultipleChoiceField(widget=Select2MultipleWidget,
                                          label='Countries of interest', required=False,
                                          choices=INTEREST_COUNTRIES)
    exists = forms.ChoiceField(widget=Select2Widget,
                               label='Exits Executed', required=False,
                               choices=EXIT_EXECUTED)


class ChooseProfileForm(forms.Form):
    profile_choice = forms.ChoiceField(
        choices=PROFILE_CHOICES, widget=forms.RadioSelect, label='')

    def clean(self):
        if not(self.cleaned_data.get('profile_choice', '')):
            raise forms.ValidationError('You need to select a choice')


class SupporterCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, label="First Name")
    last_name = forms.CharField(max_length=250, label="Last Name")

    class Meta:
        model = Supporter
        exclude = ['user', 'verified_by', 'verified']
        widgets = {'company_operations': CountrySelectWidget()}

        labels = {
            "phone_number": "Phone Number",
            "gender": "Gender",
            "company": "Company Name",
            "role": "My role at the organization?",
            "company_operations": "Where are the company's main operations based?",
            "company_registration_year": "Year of company registration",
            "interests": "Interests",
            "thumbnail_image": "Profile Image",
            "about": "About Me"
        }


class SupporterProfileCreateForm(forms.ModelForm):

    class Meta:
        model = SupporterProfile
        exclude = ['supporter_profile']
        labels = {
            "supporter_interest": "How do you classify your interest?",
            "interest_startups": "Are you interested in SMEs or Startups?",
            "interest_sectors": "Which sectors are you interested in?",
            "interest_countries": "Target countries? ",
            "trading_partners": "Do you have specific requirements for trading partners?"
        }
    interest_sectors = forms.ModelMultipleChoiceField(queryset=BusinessCategory.objects.all().order_by('name'), required=False, widget=Select2MultipleWidget)
    interest_countries = forms.MultipleChoiceField(required=False, widget=Select2MultipleWidget, choices=INTEREST_COUNTRIES,label='Countries of interest')
    trading_partners = forms.MultipleChoiceField(required=False, widget=Select2MultipleWidget, choices=TRADING_PARTNERS, label='Trade partner requirements')

class InvestorCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, label="First Name")
    last_name = forms.CharField(max_length=250, label="Last Name")
    funder_type = forms.ChoiceField(choices=FUNDER_TYPES, label="Which type of funder are you?", required=True)

    class Meta:
        model = Investor
        exclude = ['user', 'verified_by', 'verified']
        labels = {
            "funder_type": "Which type of funder are you?",
            "about": "Briefly describe your company?",
            "gender": "Gender",
            "phone_number": "Phone number",
            "company": "Company name",
            "role": "My title at the company?",
            "company_location": "Where are the company's main operations based?",
            "company_registration_year": "Year of company registration?",
            "thumbnail_image": "Profile image"
        }


class InvestorProfileCreateForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        exclude = ['investor_profile']
    target_countries = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=INTEREST_COUNTRIES, required=False)
    target_sectors = forms.ModelMultipleChoiceField(queryset=BusinessCategory.objects.all(), widget=Select2MultipleWidget,required=False)
    impact_investor = forms.ChoiceField(choices=IMPACT_INVESTOR, widget=Select2Widget, label="Do you classify your company as an impact investor?", required=False)
    average_payback = forms.ChoiceField(choices=AVERAGE_PAYBACK, label="What is the average payback period?", required=False)

    # gender_lens_investor = forms.ChoiceField(
    #     choices=IMPACT_INVESTOR, widget=Select2Widget, label="Do you Consider your firm a 'Gender-Lens' Investor?"
    # )
