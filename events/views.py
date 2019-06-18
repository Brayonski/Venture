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
    """List all events items"""
    template_name = 'events_index.html'
    paginate_by = 10
    queryset = Events.objects.filter(published=True).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.filter(published=True)
        if 'event' in self.kwargs:
            events = Events.objects.get(pk=self.kwargs['event'])
            Attendees.objects.create(event=events, attendee=self.request.user)

        context['attendees'] = Attendees.objects.all()
        return context


class NetworkEventsView(LoginRequiredMixin, ListView):
    """List all network events items"""
    template_name = 'network_events.html'
    paginate_by = 10
    queryset = NetworkEvents.objects.filter(published=True).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(NetworkEventsView, self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.filter(published=True)
        return context


class SingleEventView(LoginRequiredMixin, DetailView):
    """Read the content of a single Event"""
    model = Events
    template_name = 'event_content.html'

    def get_context_data(self, **kwargs):
        """Returns the Event selected"""
        context = super(SingleEventView,
                        self).get_context_data(**kwargs)

        current_url = resolve(self.request.path_info).url_name
        if current_url == 'network_event_view_content':
            context['content'] = NetworkEvents.objects.get(
                pk=self.kwargs.get("pk"))
            context['recommended'] = NetworkEvents.objects.order_by(
                '-date')[:6]
        else:
            context['content'] = Events.objects.get(
                pk=self.kwargs.get("pk"))
            context['recommended'] = Events.objects.order_by(
                '-date')[:6]
        return context


class EventFilterView(LoginRequiredMixin, ListView):
    """ List Events on Filter Category"""
    template_name = 'events_index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EventFilterView, self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.filter(published=True)
        return context

    def get_queryset(self, **kwargs):
        queryset = Events.objects.filter(
            category__pk=self.kwargs.get("pk")).order_by('-date')
        return queryset


class NetworkEventFilterView(LoginRequiredMixin, ListView):
    """ List Network Events on Filter Category"""
    template_name = 'network_events.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NetworkEventFilterView,
                        self).get_context_data(**kwargs)
        context['event_type'] = EventCategory.objects.filter(published=True)
        return context

    def get_queryset(self, **kwargs):
        queryset = NetworkEvents.objects.filter(
            category__pk=self.kwargs.get("pk")).order_by('-date')
        return queryset


class EventRegisterView(LoginRequiredMixin, TemplateView):
    template_name = 'event_content.html'
    queryset = Events.objects.all()

    def dispatch(self, request, *args, **kwargs):
        current_url = resolve(self.request.path_info).url_name
        events = Events.objects.get(
            pk=self.kwargs.get("event"))
        if current_url == 'event_register':
            Attendees.objects.create(
                event=events, attendee=self.request.user)
            return redirect(reverse('event_view_content', kwargs={'pk': events.id}))

        return super(EventRegisterView, self).dispatch(request, *args, **kwargs)
