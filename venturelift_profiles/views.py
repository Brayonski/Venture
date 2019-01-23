# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from venturelift_profiles.models import Supporter, Business, Post
from actstream.actions import follow, unfollow
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from actstream.models import following, followers
from django.contrib.auth.mixins import LoginRequiredMixin
from actstream.models import user_stream
from django.db.models import Q

class SummaryView(TemplateView):
    template_name = 'profile/home.html'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(SummaryView , self).get_context_data(*args, **kwargs)
        companies_following = following(self.request.user, Business)
        supporters_following = following(self.request.user, Supporter)
        posts = Post.objects.filter(Q(company__in=companies_following) | Q(author__in=supporters_following))
        self.queryset = posts
        return context

class SupporterView(LoginRequiredMixin, ListView):
    template_name = 'profile/supporters.html'
    queryset = Supporter.objects.filter(verified=True)

    def get_context_data(self, *args, **kwargs):
        context = super(SupporterView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'supporter_follow':
                follow(self.request.user, Supporter.objects.get(id=self.kwargs['pk']))
            if current_url == 'supporter_unfollow':
                unfollow(self.request.user, Supporter.objects.get(id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context

class BusinessView(LoginRequiredMixin, ListView):
    template_name = 'profile/business.html'
    queryset = Business.objects.filter(verified=True)

    def get_context_data(self, *args, **kwargs):
        context = super(BusinessView, self).get_context_data(*args, **kwargs)
        current_url = resolve(self.request.path_info).url_name
        if 'pk' in self.kwargs:
            if current_url == 'business_follow':
                follow(self.request.user, Business.objects.get(id=self.kwargs['pk']))
            if current_url == 'business_unfollow':
                unfollow(self.request.user, Business.objects.get(id=self.kwargs['pk']))
        context['following'] = following(self.request.user)
        return context