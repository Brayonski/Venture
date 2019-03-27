from venturelift_profiles.models import *
from django.contrib.auth.models import User


def account_type(request):
    context = {}
    if request.user.is_authenticated():
        if request.user.business_creator.exists():
            context['business'] = Business.objects.filter(
                creator=request.user)[0]
        if request.user.supporter_creator.exists():
            context['supporter'] = Supporter.objects.get(
                user=request.user)
            context['supporter_profile'] = SupporterProfile.objects.get(
                supporter_profile_id=context['supporter'].id)
        if request.user.investor_creator.exists():
            context['investor'] = Investor.objects.get(user=request.user)
            context['investor_profile'] = InvestorProfile.objects.get(
                investor_profile_id=context['investor'].id)
        return {"context": context}
    return context


def verified_account(request):
    verified_account = False
    if 'admin' in request.META['PATH_INFO']:
        return {}
    if request.user.is_authenticated():
        if (request.user.investor_creator.exists() and Investor.objects.get(user=request.user).verified) or (request.user.supporter_creator.exists() and Supporter.objects.get(user=request.user).verified) or (request.user.business_creator.exists() and Business.objects.get(creator=request.user).verified):
            verified_account = True
    return {"verified": verified_account}
