from venturelift_profiles.models import *
from django.forms import ModelForm
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget


class CreateBusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['verified', 'verified_by', 'creator']


class CreateBlogForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['date', 'likes', 'supporter_author', 'investor_author']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateBlogForm, self).__init__(*args, **kwargs)
        '''
        modelchoicefields = [field for field_name, field in self.fields.iteritems() if
                             isinstance(field, forms.ModelChoiceField)]

        for field in modelchoicefields:
            field.empty_label = None
        '''
        if self.user.supporter_creator.exists() or self.user.investor_creator.exists():
            self.fields.pop("company")


class MarketDescriptionForm(ModelForm):
    class Meta:
        model = MarketDescription
        exclude = ['company_name']


class BusinessModelForm(ModelForm):
    class Meta:
        model = BusinessModel
        exclude = ['company_name']


class BusinessTeamForm(ModelForm):
    class Meta:
        model = BusinessTeam
        exclude = ['company_name']


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
    profession = forms.ChoiceField(
        widget=Select2Widget, label='Resource offered', choices=PROFESSIONAL_SUPPORT, required=False)
    size = forms.ChoiceField(
        widget=Select2Widget, label='Company Stage interested in', choices=INTEREST_STARTUPS, required=False)
    countries = forms.MultipleChoiceField(widget=Select2MultipleWidget,
                                          label='Countries of interest', required=False,
                                          choices=INTEREST_COUNTRIES)


class InvestorFilters(forms.Form):
    invest_forms = forms.ChoiceField(
        widget=Select2Widget, label='Forms of Investement offered', choices=INVESTOR_FORMS, required=False)
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
    subscribe = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')), widget=forms.RadioSelect, label="Would you like us to add you to our email newsletter?"
    )
    first_name = forms.CharField(max_length=250, label="First Name")
    last_name = forms.CharField(max_length=250, label="Last Name")

    class Meta:
        model = Supporter
        exclude = ['user', 'verified_by', 'verified']
        fields = [
            'first_name',
            'last_name',
            'thumbnail_image',
            'about',
            'phone_number',
            'company',
            'company_website',
            'company_registration_year',
            'company_operations',
            'role',
            'physical_address',
            'postal_address',
            'year_operation',
            'facebook_profile',
            'linkedin_profile',
            'twitter_profile',
            'instagram_profile',
            'subscribe'
        ]
        labels = {
            "phone_number": "Phone Number",
            "company": "Company Name",
            "role": "My role at the organization?",
            "company_operations": "Where are the company's main operations based?",
            "company_registration_year": "Year of company registration",
            "year_operation": "Year company commenced operations",
            "interests": "Interests",
            "thumbnail_image": "Profile Image",
            "about": "About Me"
        }


class SupporterProfileCreateForm(forms.ModelForm):

    class Meta:
        model = SupporterProfile
        fields = [
            'supporter_interest',
            'professional_support',
            'interest_startups',
            'interest_sectors',
            'interest_countries',
            'trading_partners'
        ]
        labels = {
            "supporter_interest": "How do you classify your interest?",
            "professional_support": "Please specify if you selected, 'professional support', above",
            "interest_startups": "Are you interested in SMEs or Startups?",
            "interest_sectors": "Which sectors are you interested in?",
            "interest_countries": "Target countries? ",
            "trading_partners": "Do you have specific requirements for trading partners?"
        }


class InvestorCreateForm(forms.ModelForm):
    subscribe = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')), widget=forms.RadioSelect, label="Would you like us to add you to our email newsletter?"
    )
    first_name = forms.CharField(max_length=250, label="First Name")
    last_name = forms.CharField(max_length=250, label="Last Name")

    class Meta:
        model = Investor
        exclude = ['user', 'verified_by', 'verified']
        fields = [
            'first_name',
            'last_name',
            'thumbnail_image',
            'about',
            'phone_number',
            'company',
            'role',
            'company_website',
            'company_registration_year',
            'year_operation',
            'company_location',
            'physical_address',
            'facebook_profile',
            'linkedin_profile',
            'twitter_profile',
            'instagram_profile',
            'subscribe'
        ]
        labels = {
            "about": "Briefly describe your self?",
            "phone_number": "Phone Number",
            "company": "Company Name",
            "role": "My role at the company?",
            "company_location": "Where are the company's main operations based?",
            "company_registration_year": "Year of company registration?",
            "year_operation": "Year company commenced operations?",
            "thumbnail_image": "Profile Image"
        }


class InvestorProfileCreateForm(forms.ModelForm):
    impact_investor = forms.TypedChoiceField(choices=IMPACT_INVESTOR, widget=forms.RadioSelect, label="Do you classify yourself as an impact investor?"
                                             )

    gender_lens_investor = forms.TypedChoiceField(
        choices=IMPACT_INVESTOR, widget=forms.RadioSelect, label="Do you Consider your firm a 'Gender-Lens' Investor?"
    )

    class Meta:
        model = InvestorProfile
        fields = [
            'company_classification',
            'investor_forms',
            'elevator_pitch',
            'target_countries',
            'target_sectors',
            'managed_funds',
            'assets_under_management',
            'investor_portfolio',
            'exits_executed',
            'impact_investor',
            'impact_metrics',
            'impact_measurement',
            'gender_lens_investor',
        ]
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
