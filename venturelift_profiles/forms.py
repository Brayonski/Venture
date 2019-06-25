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
            "thumbnail_image": "Company Logo",
            "name": "Company Name",
            "sector": "Industry",
            "size": "Company Size",
            "company_primary_email": "Company Primary Email Address",
            "company_website": "Company Website",
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
            "blog_type": "Blog Type",
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


class BusinessFilters(forms.Form):
    service = forms.ModelChoiceField(queryset=VlaServices.objects.all(), required=False,
                                     label='Resources needed')
    sector = forms.ModelChoiceField(queryset=BusinessCategory.objects.all(), required=False,
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
    invest_forms = forms.ChoiceField(
        widget=Select2Widget, label='Funding Offered', choices=INVESTOR_FORMS, required=False)
    sectors = forms.ChoiceField(
        widget=Select2Widget, label='Sectors of Interest', choices=INTEREST_SECTORS, required=False)
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
    interest_sectors = forms.ModelMultipleChoiceField(queryset=BusinessCategory.objects.all(), required=False, widget=Select2MultipleWidget)
    interest_countries = forms.MultipleChoiceField(required=False, widget=Select2MultipleWidget, choices=INTEREST_COUNTRIES)
    trading_partners = forms.MultipleChoiceField(required=False, widget=Select2MultipleWidget, choices=TRADING_PARTNERS)

class InvestorCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, label="First Name")
    last_name = forms.CharField(max_length=250, label="Last Name")

    class Meta:
        model = Investor
        exclude = ['user', 'verified_by', 'verified']
        labels = {
            "about": "Briefly describe your self?",
            "phone_number": "Phone Number",
            "company": "Company Name",
            "role": "My role at the company?",
            "company_location": "Where are the company's main operations based?",
            "company_registration_year": "Year of company registration?",
            "thumbnail_image": "Profile Image"
        }


class InvestorProfileCreateForm(forms.ModelForm):
    class Meta:
        model = InvestorProfile
        exclude = ['investor_profile']
        labels = {
            'company_classification': "How would you classify your firm?",
            'investor_forms': "What forms of investment do you make?",
            'elevator_pitch': "What's your investment thesis in brief(Elevator Pitch)?",
            'target_countries': "Which are your target countries?",
            'target_sectors': "Target Sectors",
            'managed_funds': "How Many different funds have you managed to date?",
            'assets_under_management': "What's the value of your Assets under Management(AUM)?",
            'investor_portfolio': "How many active portfolio investments do you currently hold?",
            'exits_executed': "How many exits have you executed to date?",
            'impact_investor': "Do you classify yourself as an impact investor?",
            'impact_measurement': "Which impact measurement standard do you follow?",
            'impact_metrics': "Which are your key impact metrics?",
            'gender_lens_investor': "Do you Consider your firm a 'Gender-Lens' Investor?"
        }
    investor_forms = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=INVESTOR_FORMS)
    target_countries = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=INTEREST_COUNTRIES)
    target_sectors = forms.ModelMultipleChoiceField(queryset=BusinessCategory.objects.all(), widget=Select2MultipleWidget)
    impact_investor = forms.ChoiceField(choices=IMPACT_INVESTOR, widget=Select2Widget, label="Do you classify yourself as an impact investor?"
                                             )

    gender_lens_investor = forms.ChoiceField(
        choices=IMPACT_INVESTOR, widget=Select2Widget, label="Do you Consider your firm a 'Gender-Lens' Investor?"
    )
