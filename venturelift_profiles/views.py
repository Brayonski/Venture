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
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()):
            return redirect(reverse('profile_create'))
        return super(SummaryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SummaryView, self).get_context_data(*args, **kwargs)
        companies_following = following(self.request.user, Business)
        supporters_following = following(self.request.user, Supporter)
        posts = Post.objects.filter(
            Q(company__in=companies_following) | Q(author__in=supporters_following))
        context['object_list'] = posts
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
        return redirect(reverse('supporter_create'))


class SupporterView(LoginRequiredMixin, ListView):
    template_name = 'profile/supporters.html'
    queryset = Supporter.objects.filter(verified=True)

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()):
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


class BusinessView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'profile/business.html'
    queryset = Business.objects.filter(verified=True)
    form_class = BusinessFilters

    def dispatch(self, request, *args, **kwargs):
        if not(request.user.business_creator.exists()) and not(request.user.supporter_creator.exists()):
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


class CreateSupporterView(LoginRequiredMixin, CreateView):
    template_name = 'profile/create_supporter.html'
    form_class = SupporterCreateForm

    def get_form(self, form_class=None):
        supporter = Supporter.objects.filter(user=self.request.user)
        print(supporter)
        if (supporter.exists()):
            redirect(reverse('supporter_create_step_2',
                             kwargs={'pk': supporter.id}))
        else:
            form_class = SupporterCreateForm

        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.save()
        supporter = Supporter.objects.get(user=self.request.user)
        return redirect(reverse('supporter_create_step_2', kwargs={'pk': supporter.id}))


class SupporterUpdateProfileView(LoginRequiredMixin, CreateView):
    template_name = 'profile/create_supporter.html'
    form_class = SupporterProfileCreateForm

    def get_object(self):
        supporter = Supporter.objects.get(id=self.kwargs['pk'])
        obj = SupporterProfile.objects.get(
            supporter_profile=supporter)
        return obj

    def form_valid(self, form):
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
        else:
            self.object.author = Supporter.objects.get(user=self.request.user)
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
        """Returns the TextMedia instance that the view displays"""
        context = super(BusinessProfileView, self).get_context_data(**kwargs)
        context['business_profile'] = Business.objects.get(
            pk=self.kwargs.get("pk"))
        return context
