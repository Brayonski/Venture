# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import TextCenter, AudioVisual, DocumentCategory, VideoCategory, SubDocumentCategory


class TextCenterAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category', 'author']
    list_filter = ['title', 'date', 'category', 'author', 'payment_status']
    readonly_fields = ["created_by"]
    list_display = ['title', 'category', 'date',
                    'author', 'payment_status', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


class DocumentCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'author', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class SubDocumentCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'author', 'published', 'category']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class VideoCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_filter = ['title', 'author']
    readonly_fields = ["author"]
    list_display = ['title', 'author', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class AudioVisualAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author', 'payment_status']
    list_filter = ['date', 'category', 'payment_status']
    readonly_fields = ["author"]
    list_display = ['title', 'date', 'category',
                    'sub_category', 'payment_status', 'published']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


# admin.site.register(Category, CategoryAdmin)
admin.site.register(TextCenter, TextCenterAdmin)
admin.site.register(AudioVisual, AudioVisualAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(SubDocumentCategory, SubDocumentCategoryAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)
