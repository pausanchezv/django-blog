# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Client, Article, Topic, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {'fields': ['client']}),
        (None, {'fields': ['title']}),
        (None, {'fields': ['body']}),
        (None, {'fields': ['image']}),
        (None, {'fields': ['pub_date']}),
        (None, {'fields': ['topics']}),
    ]

    inlines = [CommentInline]
    search_fields = ['title']
    list_filter = ['pub_date']
    list_display = ('title', 'client')


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('COMMENT', {'fields': ['client']}),
        (None, {'fields': ['text']}),
        (None, {'fields': ['article']}),
        (None, {'fields': ['pub_date']}),
    ]

    search_fields = ['text']
    list_filter = ['pub_date']
    list_display = ('text', 'client', 'pub_date')

# Register your models here.
admin.site.register(Client)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Topic)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)