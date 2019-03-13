from venturelift_profiles.models import *
from django.forms import ModelForm
from django import forms


class CreateBusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ['verified', 'verified_by', 'creator']


class CreateBlogForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['date', 'likes', 'author']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateBlogForm, self).__init__(*args, **kwargs)
        modelchoicefields = [field for field_name, field in self.fields.iteritems() if
                             isinstance(field, forms.ModelChoiceField)]

        for field in modelchoicefields:
            field.empty_label = None

        if self.user.supporter_creator.exists():
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
    ('Supporter', 'Supporter'),
    ('Business', 'Business'),
)


class BusinessFilters(forms.Form):
    sector = forms.ModelChoiceField(queryset=BusinessCategory.objects.all(), required=False,
                                    label='Sector')

    service = forms.ModelChoiceField(queryset=VlaServices.objects.all(), required=False,
                                     label='Services needed')

    size = forms.ChoiceField(label='Company Size',
                             choices=COMPANY_SIZE, required=False)


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
            'phone_number',
            'company',
            'company_website',
            'company_registration_year',
            'role',
            'company_operations',
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
            "interests": "Interests"
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


# class InvestorrCreateForm(forms.ModelForm):
#     subscribe = forms.TypedChoiceField(
#         coerce=lambda x: x == 'True',
#         choices=((False, 'No'), (True, 'Yes')), widget=forms.RadioSelect, label="Would you like us to add you to our email newsletter?"
#     )
#     first_name = forms.CharField(max_length=250, label="First Name")
#     last_name = forms.CharField(max_length=250, label="Last Name")

#     class Meta:
#         model = Supporter
#         exclude = ['user', 'verified_by', 'verified']
#         fields = [
#             'first_name',
#             'last_name',
#             'phone_number',
#             'company',
#             'role',
#             'company_website',
#             'company_registration_year',
#             'year_operation',
#             'company_location',
#             'physical_address',
#             'facebook_profile',
#             'linkedin_profile',
#             'twitter_profile',
#             'instagram_profile',
#             'subscribe'
#         ]
#         labels = {
#             "phone_number": "Phone Number",
#             "company": "Company Name",
#             "role": "My role at the company?",
#             "company_location": "Where are the company's main operations based?",
#             "company_registration_year": "Year of company registration",
#             "year_operation": "Year company commenced operations",
#             "interests": "Interests"
#         }
