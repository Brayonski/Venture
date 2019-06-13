# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, DetailView
from events.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from actstream.models import user_stream
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.core.paginator import Paginator


class HomeView(LoginRequiredMixin, ListView):
    """List all media items"""
    template_name = 'events_index.html'
    paginate_by = 10
    queryset = Events.objects.all().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.all()
        return context


class SingleEventView(LoginRequiredMixin, DetailView):
    """Read the content of a single Event"""
    model = Events
    template_name = 'event_content.html'

    def get_context_data(self, **kwargs):
        """Returns the Event selected"""
        context = super(SingleEventView,
                        self).get_context_data(**kwargs)
        context['recommended'] = Events.objects.order_by('-date')[:6]
        context['content'] = Events.objects.get(
            pk=self.kwargs.get("pk"))
        return context


class EventFilterView(LoginRequiredMixin, ListView):
    """ List Events on Filter Category"""
    template_name = 'events_index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EventFilterView, self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.all()
        return context

    def get_queryset(self, **kwargs):
        queryset = Events.objects.filter(
            category__pk=self.kwargs.get("pk")).order_by('-date')
        return queryset
