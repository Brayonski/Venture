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
from venturelift_profiles.tasks import *
from django_registration.backends.activation.views import ActivationView

class ProfileActivationView(ActivationView):
    def activate(self, *args, **kwargs):
        username = self.validate_key(kwargs.get('activation_key'))
        user = self.get_user(username)
        user.is_active = True
        user.save()
        return user

class SummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/home.html'
    queryset = Post.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            track_login = TrackingUser(user_details=request.user, access_time=timezone.now(), action_name="register")
            track_login.save()
            return redirect(reverse('profile_create'))

        return super(SummaryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SummaryView, self).get_context_data(*args, **kwargs)
        companies_following = following(self.request.user, Business)
        supporters_following = following(self.request.user, Supporter)
        investors_following = following(self.request.user, Investor)
        posts = Post.objects.filter(
            Q(company__in=companies_following) | Q(supporter_author__in=supporters_following) | Q(investor_author__in=investors_following)).order_by('-date')[:5]
        context['object_list'] = posts
        context.update({'investor_following': investors_following, 'supporter_following':supporters_following, 'business_following': companies_following})
        track_login = TrackingUser(user_details=self.request.user,access_time=timezone.now(),action_name="login")
        track_login.save()

        if self.request.user.business_creator.exists():
            business = Business.objects.filter(creator=self.request.user).first()
            description =  MarketDescription.objects.filter(company_name=business).first()
            r_supporter = SupporterProfile.objects.filter(interest_sectors=business.sector)[:3]
            r_investor = InvestorProfile.objects.filter(target_sectors=business.sector)[:3]
            r_businesses = Business.objects.filter(sector=business.sector).exclude(creator=self.request.user)[:3]
            context.update({'business': business, 'description': description, 'r_supporter': r_supporter,
                            'r_investor':r_investor, 'r_businesses':r_businesses})
            checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
            if checkUser is False:
                createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                           email=self.request.user.email, user_type='Business')
                createUser.save()

        if self.request.user.supporter_creator.exists():
            supporter = Supporter.objects.filter(user=self.request.user).first()
            context['supporter'] = supporter
            context['profile'] = SupporterProfile.objects.get(supporter_profile=supporter)
            interests = context['profile'].interest_sectors.all()
            context['r_supporter'] = SupporterProfile.objects.filter(interest_sectors__in=interests).distinct().exclude(supporter_profile=supporter)[:3]
            context['r_businesses'] = Business.objects.filter(sector__in=interests).distinct()[:3]
            context['r_investor'] = InvestorProfile.objects.filter(target_sectors__in=interests).distinct()[:3]
            checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
            if checkUser is False:
                createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                           email=self.request.user.email, user_type='Partner')
                createUser.save()

        if self.request.user.investor_creator.exists():
            investor = Investor.objects.filter(user=self.request.user).first()
            context['investor'] = investor
            context['profile'] = InvestorProfile.objects.get(investor_profile=investor)
            interests = context['profile'].target_sectors.all()
            context['r_supporter'] = SupporterProfile.objects.filter(interest_sectors__in=interests).distinct()[:3]
            context['r_businesses'] = Business.objects.filter(sector__in=interests).distinct()[:3]
            context['r_investor'] = InvestorProfile.objects.filter(target_sectors__in=interests).distinct().exclude(investor_profile=investor)[:3]
            checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
            if checkUser is False:
                createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                           email=self.request.user.email, user_type='Investor')
                createUser.save()

        if 'pk' in kwargs:
            current_url = resolve(self.request.path_info).url_name
            post = Post.objects.get(pk=kwargs['pk'])
            if current_url == 'like_post':
                post.likes.add(self.request.user)
            if current_url == 'dislike_post':
                post.likes.remove(self.request.user)
        return context


class ProfileCreateView(LoginRequiredMixin, FormView):
    template_name = 'profile/profile_create.html'
    form_class = ChooseProfileForm

    def form_valid(self, form):
        if form.cleaned_data['profile_choice'] == 'Business':
            return redirect(reverse('create_business_step1'))
        if form.cleaned_data['profile_choice'] == 'Investor':
            return redirect(reverse('investor_create'))
        return redirect(reverse('supporter_create'))


class SupporterView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/supporter/supporters.html'
    queryset = Supporter.objects.filter(verified=True)
    form_class = SupporterFilters

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.POST.get('supporter-name'):
                fullname = request.POST.get('supporter-name').split(' ')
                if len(fullname) >= 2:
                    last_name = fullname[1]
                else:
                    last_name = request.POST.get('supporter-name')
                first_name = fullname[0]

                supporter = Supporter.objects.filter((Q(
                    user__first_name__icontains=first_name) | Q(user__last_name__icontains=last_name)), verified=True)
            else:
                supporter = Supporter.objects.filter(verified=True)
                if form.cleaned_data['profession']:
                    supporter = supporter.filter(
                        supporter_profile__professional_support=form.cleaned_data['profession'])
                if form.cleaned_data['size']:
                    supporter = supporter.filter(
                        supporter_profile__interest_startups__in=form.cleaned_data['size'])
                if form.cleaned_data['countries']:
                    supporter = supporter.filter(
                        supporter_profile__interest_countries__in=form.cleaned_data['countries']
                    )
            return render(request, self.template_name, {'object_list': supporter, 'form': form, 'following': following(self.request.user)})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
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


class InvestorView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/investor/investors.html'
    queryset = Investor.objects.filter(verified=True)
    form_class = InvestorFilters

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(InvestorView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.POST.get('investor-name'):
                fullname = request.POST.get('investor-name').split(' ')
                if len(fullname) >= 2:
                    last_name = fullname[1]
                else:
                    last_name = request.POST.get('investor-name')
                first_name = fullname[0]

                investor = Investor.objects.filter((Q(
                    user__first_name__icontains=first_name) | Q(user__last_name__icontains=last_name)), verified=True)
            else:
                investors = Investor.objects.filter(verified=True)
                if form.cleaned_data['invest_forms']:
                    print(form.cleaned_data['invest_forms'])
                    investor = investors.filter(
                        investor_profile__investor_forms__icontains=form.cleaned_data['invest_forms'])
                if form.cleaned_data['sectors']:
                    investor = investors.filter(
                        investor_profile__target_sectors__icontains=form.cleaned_data['sectors'])
                if form.cleaned_data['countries']:
                    investor = investors.filter(
                        investor_profile__target_countries__in=form.cleaned_data['countries']
                    )
                if form.cleaned_data['exists']:
                    investor = investors.filter(
                        investor_profile__exits_executed=form.cleaned_data['exists']
                    )
        return render(request, self.template_name, {'object_list': investor, 'form': form, 'following': following(self.request.user)})

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
    template_name = 'profile/business/business.html'
    queryset = Business.objects.filter(verified=True)
    form_class = BusinessFilters

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
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
                business_details = Business.objects.get(
                    id=self.kwargs['pk'])
                check_coneection = BusinessConnectRequest.objects.filter(business=business_details, investor=self.request.user, approval_status="PENDING").first()
                if check_coneection:
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username,
                                                                   subject, from_email, to)
                else:
                    connections = BusinessConnectRequest(business=business_details, created_at=timezone.now(), investor=self.request.user, approval_status="PENDING", approved=False, rejected=False)
                    connections.save()
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username, subject, from_email, to)
                follow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'business_unfollow':
                unfollow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context

class BusinessStartupView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/business/business.html'
    queryset = Business.objects.filter(verified=True).filter(size='Startup')
    form_class = BusinessFilters

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(BusinessStartupView, self).dispatch(request, *args, **kwargs)

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
        context = super(BusinessStartupView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'business_follow':
                business_details = Business.objects.get(
                    id=self.kwargs['pk'])
                check_coneection = BusinessConnectRequest.objects.filter(business=business_details, investor=self.request.user, approval_status="PENDING").first()
                if check_coneection:
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username,
                                                                   subject, from_email, to)
                else:
                    connections = BusinessConnectRequest(business=business_details, created_at=timezone.now(), investor=self.request.user, approval_status="PENDING", approved=False, rejected=False)
                    connections.save()
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username, subject, from_email, to)
                follow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'business_unfollow':
                unfollow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context


class BusinessSMEView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/business/business.html'
    queryset = Business.objects.filter(verified=True).filter(size='SME')
    form_class = BusinessFilters

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()) and not(request.user.investor_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(BusinessSMEView, self).dispatch(request, *args, **kwargs)

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
        context = super(BusinessSMEView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'business_follow':
                business_details = Business.objects.get(
                    id=self.kwargs['pk'])
                check_coneection = BusinessConnectRequest.objects.filter(business=business_details, investor=self.request.user, approval_status="PENDING").first()
                if check_coneection:
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username,
                                                                   subject, from_email, to)
                else:
                    connections = BusinessConnectRequest(business=business_details, created_at=timezone.now(), investor=self.request.user, approval_status="PENDING", approved=False, rejected=False)
                    connections.save()
                    subject, from_email, to = 'Business Connection Request', settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
                    send_business_connect_request_email_task.delay(business_details.name, self.request.user.username, subject, from_email, to)
                follow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
            if current_url == 'business_unfollow':
                unfollow(self.request.user, Business.objects.get(
                    id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context




class CreateBusinessView(LoginRequiredMixin, CreateView):
    template_name = 'profile/business/create_business.html'
    form_class = CreateBusinessForm

    def form_valid(self, form):
        businessCheck = Business.objects.filter(name=form.cleaned_data['name']).first()
        if businessCheck is None:
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            self.object.save()
        checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
        if checkUser is False:
            createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                       email=self.request.user.email, user_type='Business')
            createUser.save()
        business = Business.objects.filter(name=form.cleaned_data['name']).first()
        MarketDescription.objects.create(company_name=business)
        BusinessModel.objects.create(company_name=business)
        BusinessTeam.objects.create(company_name=business)
        BusinessFinancial.objects.create(company_name=business)
        BusinessInvestment.objects.create(company_name=business)
        BusinessGoals.objects.create(company_name=business)

        return redirect(reverse('update_business_step2', kwargs={'pk': business.id}))


class CreateInvestorView(LoginRequiredMixin, CreateView):
    template_name = 'profile/investor/create_investor.html'
    form_class = InvestorCreateForm

    def form_valid(self, form):
        investorCheck = Investor.objects.filter(user=self.request.user).first()
        if investorCheck is None:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.user.first_name = form.cleaned_data['first_name']
            self.object.user.last_name = form.cleaned_data['last_name']
            self.object.user.save()
            self.object.save()
        investor = Investor.objects.filter(user=self.request.user).first()
        checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
        if checkUser is False:
            createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                       email=self.request.user.email, user_type='Investor')
            createUser.save()
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
    template_name = 'profile/investor/update_investor.html'

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
            obj = ''
            if InvestorProfile.objects.filter(investor_profile=investor).exists():
                obj = InvestorProfile.objects.filter(investor_profile=investor).first()
            else:
                md = InvestorProfile(investor_profile=investor)
                md.save()
                obj = InvestorProfile.objects.filter(investor_profile=investor).first()
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
        context['investor'] = Investor.objects.filter(
            user=self.request.user).first()
        return context


class CreateSupporterView(LoginRequiredMixin, CreateView):
    template_name = 'profile/supporter/create_supporter.html'
    form_class = SupporterCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.save()
        checkUser = AllSystemUser.objects.filter(email=self.request.user.email).exists()
        if checkUser is False:
            createUser = AllSystemUser(created_at=timezone.now(), username=self.request.user.username,
                                       email=self.request.user.email, user_type='Partner')
            createUser.save()
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
    template_name = 'profile/supporter/update_supporter.html'

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.business_creator.exists():
            self.object.company = Business.objects.get(
                creator=self.request.user)
        if self.request.user.supporter_creator.exists():
            self.object.supporter_author = Supporter.objects.get(
                user=self.request.user)
        if self.request.user.investor_creator.exists():
            self.object.investor_author = Investor.objects.get(
                user=self.request.user)
        self.object.save()

        return redirect(reverse('profile_summary'))


class UpdateBusinessView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/business/update_business.html'

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
            obj = ''
            if MarketDescription.objects.filter(company_name=business).exists():
                obj = MarketDescription.objects.filter(company_name=business).first()
            else:
                md = MarketDescription(company_name=business)
                md.save()
                obj = MarketDescription.objects.filter(company_name=business).first()
        if current_url == 'update_business_step3':
            obj = ''
            if BusinessModel.objects.filter(company_name=business).exists():
                obj = BusinessModel.objects.filter(company_name=business).first()
            else:
                md = BusinessModel(company_name=business)
                md.save()
                obj = BusinessModel.objects.filter(company_name=business).first()
        if current_url == 'update_business_step4':
            obj = ''
            if BusinessTeam.objects.filter(company_name=business).exists():
                obj = BusinessTeam.objects.filter(company_name=business).first()
            else:
                team = BusinessTeam(company_name=business)
                team.save()
                obj = BusinessTeam.objects.filter(company_name=business).first()
        if current_url == 'update_business_step5':
            obj = ''
            if BusinessFinancial.objects.filter(company_name=business).exists():
                obj = BusinessFinancial.objects.filter(company_name=business).first()
            else:
                finance = BusinessFinancial(company_name=business)
                finance.save()
                obj = BusinessFinancial.objects.filter(company_name=business).first()
        if current_url == 'update_business_step6':
            obj = ''
            if BusinessInvestment.objects.filter(company_name=business).exists():
                obj = BusinessInvestment.objects.filter(company_name=business).first()
            else:
                invest = BusinessInvestment(company_name=business)
                invest.save()
                obj = BusinessInvestment.objects.filter(company_name=business).first()
        if current_url == 'update_business_step7':
            obj = ''
            if BusinessGoals.objects.filter(company_name=business).exists():
                obj = BusinessGoals.objects.filter(company_name=business).first()
            else:
                goal = BusinessGoals(company_name=business)
                goal.save()
                obj = BusinessGoals.objects.filter(company_name=business).first()
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
            return redirect(reverse('profile_summary'))

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


class BusinessProfileView(DetailView):
    model = Business
    template_name = 'profile/business/business_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Business Profile instance that the view displays"""
        context = super(BusinessProfileView, self).get_context_data(**kwargs)
        business = Business.objects.get(
            pk=self.kwargs.get("pk"))
        r_supporter = SupporterProfile.objects.filter(interest_sectors=business.sector)[:3]
        r_investor = InvestorProfile.objects.filter(target_sectors=business.sector)[:3]
        r_businesses = Business.objects.filter(sector=business.sector).exclude(creator=self.request.user)[:3]
        context.update({'r_supporter': r_supporter,
                        'r_investor':r_investor, 'r_businesses':r_businesses, 'business': business})
        context['post'] = Post.objects.filter(
            company=context['business'])[:5]
        context['investor_following'] = following(self.request.user, Investor)[:3]
        context['supporter_following'] = following(
            self.request.user, Supporter)[:3]
        context['business_following'] = following(self.request.user, Business)[:3]
        context['following'] = following(self.request.user)
        return context


class SupporterProfileView(DetailView):
    model = Supporter
    template_name = 'profile/supporter/supporter_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Supporter instance that the view displays"""
        context = super(SupporterProfileView, self).get_context_data(**kwargs)
        context['supporter'] = Supporter.objects.get(
            pk=self.kwargs.get("pk"))
        context['profile'] = SupporterProfile.objects.get(
            supporter_profile_id=context['supporter'].id)
        context['post'] = Post.objects.filter(
            supporter_author=context['supporter'])[:5]
        interests = context['profile'].interest_sectors.all()
        context['r_supporter'] = SupporterProfile.objects.filter(interest_sectors__in=interests).distinct().exclude(supporter_profile=context['supporter'])[:3]
        context['r_businesses'] = Business.objects.filter(sector__in=interests).distinct()[:3]
        context['r_investor'] = InvestorProfile.objects.filter(target_sectors__in=interests).distinct()[:3]

        context['investor_following'] = following(self.request.user, Investor)
        context['supporter_following'] = following(
            self.request.user, Supporter)
        context['business_following'] = following(self.request.user, Business)
        return context


class InvestorProfileView(DetailView):
    model = Investor
    template_name = 'profile/investor/investor_profile.html'

    def get_context_data(self, **kwargs):
        """Returns the Investor instance that the view displays"""
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

        interests = context['investor_profile'].target_sectors.all()
        context['r_supporter'] = SupporterProfile.objects.filter(interest_sectors__in=interests).distinct()[:3]
        context['r_businesses'] = Business.objects.filter(sector__in=interests).distinct()[:3]
        context['r_investor'] = InvestorProfile.objects.filter(target_sectors__in=interests).distinct().exclude(investor_profile=context['investor'])[:3]
        return context
