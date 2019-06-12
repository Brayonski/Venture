# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, DetailView
from knowledge_center.models import *
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
    queryset = TextCenter.objects.all().order_by('-date')
