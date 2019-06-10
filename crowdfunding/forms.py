from crowdfunding.models import *
from django.forms import ModelForm
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_countries.widgets import CountrySelectWidget

class CreateCampaignForm(ModelForm):
    class Meta:
        model = Campaign
        exclude = ['created_at', 'total_funds_received', 'campaign_status','campaign_owner','funds_disbursement_status']
        labels = {
            "campaign_name": "Campaign Name",
            "company_name": "Company Name",
            "company_email": "Company Email",
            "sector": "Campaign Sector",
            "duration": "Campaign Closing Date",
            "target_amount": "Target Amount",
            "campaign_image": "Campaign Thumbnail / Image",
            "short_description": "Short Description",
            "long_description": "Long Description",
        }

    sector = forms.ModelChoiceField(queryset=CampaignSector.objects.all(), required=True,label='Campaign Sector',widget=Select2Widget)


class CreateCampaignPaymentForm(ModelForm):
    class Meta:
        model = CampaignPayment
        exclude = ['campaign', 'donator', 'payment_status','payment_order_number','paid']
        labels = {
            "payment_method": "Payment Method",
            "amount": "Amount to Donate",
        }