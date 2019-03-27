# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, DetailView
from venturelift_profiles.models import *
from actstream.actions import follow, unfollow
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from actstream.models import following, followers
from django.contrib.auth.mixins import LoginRequiredMixin
from actstream.models import user_stream
from django.db.models import Q
from venturelift_profiles.forms import *
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormMixin


class SummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/home.html'
    queryset = Post.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))

        return super(SummaryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SummaryView, self).get_context_data(*args, **kwargs)
        companies_following = following(self.request.user, Business)
        supporters_following = following(self.request.user, Supporter)
        investors_following = following(self.request.user, Investor)
        posts = Post.objects.filter(
            Q(company__in=companies_following) | Q(supporter_author__in=supporters_following) | Q(investor_author__in=investors_following))
        context['object_list'] = posts
        if 'pk' in kwargs:
            current_url = resolve(self.request.path_info).url_name
            post = Post.objects.get(pk=kwargs['pk'])
            if current_url == 'like_post':
                post.likes.add(self.request.user)
            if current_url == 'dislike_post':
                post.likes.remove(self.request.user)
        return context


class VerificationAccountWaiting(LoginRequiredMixin, TemplateView):
    template_name = 'profile/account_verification_waiting.html'


class ProfileCreateView(LoginRequiredMixin, FormView):
    template_name = 'profile/profile_create.html'
    form_class = ChooseProfileForm

    def form_valid(self, form):
        if form.cleaned_data['profile_choice'] == 'Business':
            return redirect(reverse('create_business_step1'))
        if form.cleaned_data['profile_choice'] == 'Investor':
            return redirect(reverse('investor_create'))
        return redirect(reverse('supporter_create'))


class SupporterView(LoginRequiredMixin, ListView):
    template_name = 'profile/supporters.html'
    queryset = Supporter.objects.filter(verified=True)

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(SupporterView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SupporterView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'supporter_follow':
                follow(self.request.user, Supporter.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'supporter_unfollow':
                unfollow(self.request.user, Supporter.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context


class InvestorView(LoginRequiredMixin, ListView):
    template_name = 'profile/investors.html'
    queryset = Investor.objects.filter(verified=True)

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(InvestorView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(InvestorView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'investor_follow':
                follow(self.request.user, Investor.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'investor_unfollow':
                unfollow(self.request.user, Investor.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context


class BusinessView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/business.html'
    queryset = Business.objects.filter(verified=True)
    form_class = BusinessFilters

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(BusinessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.POST.get('company-name'):
                business = Business.objects.filter(
                    name__icontains=request.POST.get('company-name'), verified=True)
            else:
                business = Business.objects.filter(verified=True)
                if form.cleaned_data['sector']:
                    business = business.filter(
                        sector=form.cleaned_data['sector'])
                if form.cleaned_data['size']:
                    business = business.filter(size=form.cleaned_data['size'])
                if form.cleaned_data['service']:
                    business = business.filter(Q(business_goals__primary_services_interested_in=form.cleaned_data['service']) |
                                               Q(business_goals__secondary_services_interested_in=form.cleaned_data['service']))
            return render(request, self.template_name, {'object_list': business, 'form': form, 'following': following(self.request.user)})

    def get_context_data(self, *args, **kwargs):
        context = super(BusinessView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'business_follow':
                follow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'business_unfollow':
                unfollow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context


class CreateBusinessView(LoginRequiredMixin, CreateView):
    template_name = 'profile/create_business.html'
    form_class = CreateBusinessForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        business = Business.objects.get(name=form.cleaned_data['name'])
        MarketDescription.objects.create(company_name=business)
        BusinessModel.objects.create(company_name=business)
        BusinessTeam.objects.create(company_name=business)
        BusinessFinancial.objects.create(company_name=business)
        BusinessInvestment.objects.create(company_name=business)
        BusinessGoals.objects.create(company_name=business)

        return redirect(reverse('update_business_step2', kwargs={'pk': business.id}))


class CreateInvestorView(LoginRequiredMixin, CreateView):
    template_name = 'profile/create_investor.html'
    form_class = InvestorCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.user.save()
        self.object.save()
        investor = Investor.objects.get(user=self.request.user)
        InvestorProfile.objects.create(investor_profile=investor)
        return redirect(reverse('update_investor_step2', kwargs={'pk': investor.id}))

    def get_context_data(self, **kwargs):
        current_url = resolve(self.request.path_info).url_name
        context = super(CreateInvestorView, self).get_context_data(**kwargs)
        if current_url == 'investor_create':
            context["step1"] = True
        if current_url == 'update_investor_step2':
            context["step2"] = True
        return context


class InvestorUpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/update_investor.html'

    def get_form(self, form_class=None):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_investor_step1':
            form_class = InvestorCreateForm
        if current_url == 'update_investor_step2':
            form_class = InvestorProfileCreateForm

        return form_class(**self.get_form_kwargs())

    def get_initial(self):
        return {'first_name': self.request.user.first_name, 'last_name': self.request.user.last_name}

    def get_object(self):
        investor = Investor.objects.get(id=self.kwargs['pk'])
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_investor_step1':
            obj = investor
        if current_url == 'update_investor_step2':
            obj = InvestorProfile.objects.get(investor_profile=investor)
        return obj

    def form_valid(self, form):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_investor_step1':
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.user.first_name = form.cleaned_data['first_name']
            self.object.user.last_name = form.cleaned_data['last_name']
            self.object.user.save()
            self.object.save()
            return redirect(reverse('update_investor_step2',
                                    kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_investor_step2':
            form.save()
            return redirect(reverse('investor_list'))

    def get_context_data(self, **kwargs):
        context = super(InvestorUpdateProfileView,
                        self).get_context_data(**kwargs)
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_investor_step1':
            context["step1"] = True
        if current_url == 'update_investor_step2':
            context["step2"] = True
        context['investor'] = Investor.objects.get(
            user=self.request.user)
        return context


class CreateSupporterView(LoginRequiredMixin, CreateView):
    template_name = 'profile/create_supporter.html'
    form_class = SupporterCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.save()
        supporter = Supporter.objects.get(user=self.request.user)
        SupporterProfile.objects.create(supporter_profile=supporter)
        return redirect(reverse('update_supporter_step2', kwargs={'pk': supporter.id}))

    def get_context_data(self, **kwargs):
        current_url = resolve(self.request.path_info).url_name
        context = super(CreateSupporterView, self).get_context_data(**kwargs)
        if current_url == 'supporter_create':
            context["step1"] = True
        if current_url == 'update_supporter_step2':
            context["step2"] = True
        return context


class SupporterUpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/update_supporter.html'

    def get_form(self, form_class=None):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_supporter_step1':
            form_class = SupporterCreateForm
        if current_url == 'update_supporter_step2':
            form_class = SupporterProfileCreateForm

        return form_class(**self.get_form_kwargs())

    def get_object(self):
        supporter = Supporter.objects.get(id=self.kwargs['pk'])
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_supporter_step1':
            obj = supporter
        if current_url == 'update_supporter_step2':
            obj = SupporterProfile.objects.get(supporter_profile=supporter)
        return obj

    def get_initial(self):
        return {'first_name': self.request.user.first_name, 'last_name': self.request.user.last_name}

    def get_context_data(self, **kwargs):
        current_url = resolve(self.request.path_info).url_name
        context = super(SupporterUpdateProfileView,
                        self).get_context_data(**kwargs)
        if current_url == 'update_supporter_step1':
            context["step1"] = True
        if current_url == 'update_supporter_step2':
            context["step2"] = True
        context['supporter'] = Supporter.objects.get(
            user=self.request.user)
        return context

    def form_valid(self, form):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_supporter_step1':
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.user.first_name = form.cleaned_data['first_name']
            self.object.user.last_name = form.cleaned_data['last_name']
            self.object.user.save()
            self.object.save()
            return redirect(reverse('update_supporter_step2',
                                    kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_supporter_step2':
            form.save()
            return redirect(reverse('supporter_list'))


class CreateBlogPostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create_post.html'
    form_class = CreateBlogForm

    def get_form_kwargs(self):
        kwargs = super(CreateBlogPostView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        queryset = Business.objects.filter(creator=self.request.user)
        return {'company': queryset}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'company' in form.cleaned_data:
            self.object.company = form.cleaned_data['company']
        if self.request.user.supporter_creator.exists():
            self.object.supporter_author = Supporter.objects.get(
                user=self.request.user)
        if self.request.user.investor_creator.exists():
            self.object.investor_author = Investor.objects.get(
                user=self.request.user)
        self.object.save()

        return redirect(reverse('profile_summary'))


class UpdateBusinessView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/update_business.html'

    def get_form(self, form_class=None):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_business_step1':
            form_class = CreateBusinessForm
        if current_url == 'update_business_step2':
            form_class = MarketDescriptionForm
        if current_url == 'update_business_step3':
            form_class = BusinessModelForm
        if current_url == 'update_business_step4':
            form_class = BusinessTeamForm
        if current_url == 'update_business_step5':
            form_class = BusinessFinancialForm
        if current_url == 'update_business_step6':
            form_class = BusinessInvestmentForm
        if current_url == 'update_business_step7':
            form_class = BusinessGoalsForm
        return form_class(**self.get_form_kwargs())

    def get_object(self):
        business = Business.objects.get(id=self.kwargs['pk'])
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_business_step1':
            obj = business
        if current_url == 'update_business_step2':
            obj = MarketDescription.objects.get(company_name=business)
        if current_url == 'update_business_step3':
            obj = BusinessModel.objects.get(company_name=business)
        if current_url == 'update_business_step4':
            obj = BusinessTeam.objects.get(company_name=business)
        if current_url == 'update_business_step5':
            obj = BusinessFinancial.objects.get(company_name=business)
        if current_url == 'update_business_step6':
            obj = BusinessInvestment.objects.get(company_name=business)
        if current_url == 'update_business_step7':
            obj = BusinessGoals.objects.get(company_name=business)
        return obj

    def form_valid(self, form):
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_business_step1':
            form.save()
            return redirect(reverse('update_business_step2', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step2':
            form.save()
            return redirect(reverse('update_business_step3', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step3':
            form.save()
            return redirect(reverse('update_business_step4', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step4':
            form.save()
            return redirect(reverse('update_business_step5', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step5':
            form.save()
            return redirect(reverse('update_business_step6', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step6':
            form.save()
            return redirect(reverse('update_business_step7', kwargs={'pk': self.kwargs['pk']}))
        if current_url == 'update_business_step7':
            form.save()
            return redirect(reverse('my_business'))

    def get_context_data(self, **kwargs):
        context = super(UpdateBusinessView, self).get_context_data(**kwargs)
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'update_business_step1':
            context["step1"] = True
        if current_url == 'update_business_step2':
            context["step2"] = True
        if current_url == 'update_business_step3':
            context["step3"] = True
        if current_url == 'update_business_step4':
            context["step4"] = True
        if current_url == 'update_business_step5':
            context["step5"] = True
        if current_url == 'update_business_step6':
            context["step6"] = True
        return context


class MyBusinessView(LoginRequiredMixin, ListView):
    template_name = 'profile/my_business.html'
    queryset = Business.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MyBusinessView, self).get_context_data(**kwargs)
        context['object_list'] = Business.objects.filter(
            creator=self.request.user)
        return context


class BusinessProfileView(DetailView):
    model = Business
    template_name = 'profile/business_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Business Profile instance that the view displays"""
        investor_list = []
        supporter_list = []
        business_list = []
        context = super(BusinessProfileView, self).get_context_data(**kwargs)
        context['business'] = Business.objects.get(
            pk=self.kwargs.get("pk"))
        context['post'] = Post.objects.filter(
            company=context['business'])[:5]
        context['business_market'] = MarketDescription.objects.filter(
            company_name=context['business'])
        context['business_model'] = BusinessModel.objects.filter(
            company_name=context['business'])
        context['business_team'] = BusinessTeam.objects.filter(
            company_name=context['business'])
        context['business_finance'] = BusinessFinancial.objects.filter(
            company_name=context['business'])
        context['business_investment'] = BusinessInvestment.objects.filter(
            company_name=context['business'])
        context['business_goals'] = BusinessGoals.objects.filter(
            company_name=context['business'])
        context['investor_following'] = following(self.request.user, Investor)
        context['supporter_following'] = following(
            self.request.user, Supporter)
        context['business_following'] = following(self.request.user, Business)
        context['followers'] = followers(context['business'])
        context['user'] = self.request.user
        for obj in context['followers']:
            if obj.investor_creator.exists():
                investor_list.append(Investor.objects.get(user=obj))
            elif obj.supporter_creator.exists():
                supporter_list.append(Supporter.objects.get(user=obj))
            elif obj.business_creator.exists():
                business_list.append(Business.objects.get(creator=obj))
        context['investor_followers'] = investor_list
        context['supporter_followers'] = supporter_list
        context['business_followers'] = business_list
        return context


class SupporterProfileView(DetailView):
    model = Supporter
    template_name = 'profile/supporter_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Supporter instance that the view displays"""
        investor_list = []
        supporter_list = []
        business_list = []
        context = super(SupporterProfileView, self).get_context_data(**kwargs)
        context['supporter'] = Supporter.objects.get(
            pk=self.kwargs.get("pk"))
        context['supporter_profile'] = SupporterProfile.objects.get(
            supporter_profile_id=context['supporter'].id)
        context['post'] = Post.objects.filter(
            supporter_author=context['supporter'])[:5]

        context['investor_following'] = following(self.request.user, Investor)
        context['supporter_following'] = following(
            self.request.user, Supporter)
        context['business_following'] = following(self.request.user, Business)
        context['followers'] = followers(context['supporter'])
        context['user'] = self.request.user
        for obj in context['followers']:
            if obj.investor_creator.exists():
                investor_list.append(Investor.objects.get(user=obj))
            elif obj.supporter_creator.exists():
                supporter_list.append(Supporter.objects.get(user=obj))
            elif obj.business_creator.exists():
                business_list.append(Business.objects.get(creator=obj))
        context['investor_followers'] = investor_list
        context['supporter_followers'] = supporter_list
        context['business_followers'] = business_list
        return context


class InvestorProfileView(DetailView):
    model = Investor
    template_name = 'profile/investor_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Investor instance that the view displays"""
        investor_list = []
        supporter_list = []
        business_list = []
        context = super(InvestorProfileView, self).get_context_data(**kwargs)
        context['investor'] = Investor.objects.get(
            pk=self.kwargs.get("pk"))
        context['investor_profile'] = InvestorProfile.objects.get(
            investor_profile=context['investor'])
        context['post'] = Post.objects.filter(
            investor_author=context['investor'])[:5]
        context['investor_following'] = following(self.request.user, Investor)
        context['supporter_following'] = following(
            self.request.user, Supporter)
        context['business_following'] = following(self.request.user, Business)
        context['followers'] = followers(context['investor'])
        context['user'] = self.request.user
        for obj in context['followers']:
            if obj.investor_creator.exists():
                investor_list.append(Investor.objects.get(user=obj))
            elif obj.supporter_creator.exists():
                supporter_list.append(Supporter.objects.get(user=obj))
            elif obj.business_creator.exists():
                business_list.append(Business.objects.get(creator=obj))
        context['investor_followers'] = investor_list
        context['supporter_followers'] = supporter_list
        context['business_followers'] = business_list
        return context
