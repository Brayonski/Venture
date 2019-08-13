# * coding: utf8 *
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from .models import TextMedia, AudioVisual, Category
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, resolve

class HomeView(ListView):
    queryset = TextMedia.objects.filter(category__pk=1).order_by('date')[:4]
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.path != '/en/media/':
            context = self.get_context_categories()
            return render(request, 'categories.html', context)
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["podcasts"] = AudioVisual.objects.filter(
            category='Podcast').order_by('date')[:3]
        context["videos"] = AudioVisual.objects.filter(
            category='Video').order_by('date')[:6]
        context["vla_tv"] = AudioVisual.objects.filter(
            category='Video', vla_tv=True).order_by('date')[:1]
        context['other_articles'] = self.get_other_articles()
        context['more_articles'] = self.get_more_articles()
        cat = Category.objects.filter(title='Trade').first()
        context['stories_top'] = TextMedia.objects.all()[:3]
        if cat is not None:
            context['stories_top'] = TextMedia.objects.filter(category=cat)[:3]
        cat2 = Category.objects.filter(title='Diaspora').first()
        context['stories_bottom'] = TextMedia.objects.filter(priority=True).order_by('date')[:3]
        if cat2 is not None:
            context['stories_bottom'] = TextMedia.objects.filter(category=cat2,priority=True).order_by('date')[:3]
        return context

    def get_context_categories(self):
        path = self.request.path.rsplit('/', 1)[0]
        category = path.rsplit('/', 1)[1]
        context = {}
        context['category'] = category   
        current_url = resolve(self.request.path_info).url_name         
        if current_url == 'media_videos':
            context['visual'] = AudioVisual.objects.filter(category='Video', sub_category__title__icontains=category).order_by('date')
        elif current_url == 'media_podcast':
            context['audio'] = AudioVisual.objects.filter(category='Podcast', sub_category__title__icontains=category).order_by('date')
        else:
            context['media'] = TextMedia.objects.filter(category__title__icontains=category).order_by('date')
        return context

    def get_other_articles(self):
        categories = Category.objects.exclude(title='Diaspora').exclude(title='Trade')[:4]
        articles = []
        for category in categories:
            article = TextMedia.objects.filter(category=category)[:1]
            if len(article) > 0:
                articles.append(article[0])
        return articles

    def get_more_articles(self):
        categories = Category.objects.exclude(title='Diaspora').exclude(title='Trade')
        articles = []
        for category in categories:
            article = TextMedia.objects.filter(category=category,priority=True).order_by('date')[:1]
            if  len(articles) >= 3:
                break
            if len(article) > 0:
                articles.append(article[0])

        return articles

class TextMediaView(DetailView):
    model = TextMedia
    template_name = 'text_media.html'

    def get_context_data(self, **kwargs):
        """Returns the TextMedia instance that the view displays"""
        context = super(TextMediaView, self).get_context_data(**kwargs)
        context['text_media'] = TextMedia.objects.get(
            pk=self.kwargs.get("pk"))
        return context