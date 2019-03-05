# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import TextMedia, AudioVisual, Category
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    queryset = TextMedia.objects.filter(category__pk=1).order_by('-date')[:4]
    template_name = 'index.html' 

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["podcasts"] =  AudioVisual.objects.filter(category='Podcast').order_by('-date')[:3]
        context["videos"] = AudioVisual.objects.filter(category='Video').order_by('-date')[:7]
        context['other_articles'] = self.get_other_articles()
        context['stories_top'] = TextMedia.objects.all()[:3]
        context['stories_bottom'] = TextMedia.objects.all().order_by('-date')[:3]
        return context
    
    def get_other_articles(self):
        categories = Category.objects.exclude(pk=1)[:4]
        articles = []
        for category in categories:
            article = TextMedia.objects.filter(category=category)[:1]
            articles.append(article[0])
        return articles

class StoryDetailView(DetailView):
    pass