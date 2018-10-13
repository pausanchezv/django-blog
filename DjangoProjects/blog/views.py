# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import datetime

import json
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from DjangoProjects.settings import STATIC_URL, MEDIA_URL
from blog.ajax import Ajax
from blog.models import Client, Article, Topic, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth

from .forms import ArticleForm, UserEditForm


import random


@require_http_methods(["GET", "POST"])
def index(request):
    """ Index view """

    articles = Article.objects.all()[0:2]

    context = {
        'articles': articles
    }

    return render(request, 'blog/index.html', context)


@require_http_methods(["GET", "POST"])
def register(request):
    """ Register view """

    # redirect if is authenticated
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blog:index'))

    # generate context only when there are errors
    context = {
        'errors': {
            'email_exists': 'This email already exists',
            'username_exists': 'This username already exists'
        }
    }

    # checking POST
    if request.method == 'POST':

        # get post values
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # register user to DB
        if username.strip() and email.strip() and password.strip():

            if not User.objects.filter(email=email).count() and not User.objects.filter(username=username).count():

                user = User.objects.create_user(username, email, password)
                user.save()

                #Client(user=user).save()

                auth.login(request, user)
                return HttpResponseRedirect(reverse('blog:userhome'))

    return render(request, 'blog/register.html', context)


@require_http_methods(["GET", "POST"])
def login(request):
    """ Log in into website """

    # redirect if is authenticated
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blog:userhome'))

    context = {
        'login_error': 'Incorrect log in credentials'
    }

    # checking POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # check authentication via username
        user = authenticate(request, username=username, password=password)

        # if user does not exist could mean that the client is trying to log in through email
        if user is None:

            # try to get an user by email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = None

            # if user does exist by email authentication takes place
            if user is not None:
                user = authenticate(request, username=user.username, password=password)

        # user definitely doesn't exist
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('blog:userhome'))

    return render(request, 'blog/login.html', context)


@require_http_methods("GET")
def logout(request):
    """ Closing user session """

    auth.logout(request)
    return HttpResponseRedirect(reverse('blog:login'))


@login_required(login_url="/blog/login")
@require_http_methods("GET")
def userhome(request):
    """ Userhome view """

    # redirect if is authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blog:login'))

    client = get_object_or_404(Client, user=request.user)
    topics = Topic.objects.all()

    context = {
        'client': client,
        'form': ArticleForm(),
        'topics': topics
    }

    return render(request, 'blog/userhome.html', context)



def user_update(request):
    """ Edit view """

    # redirect if is authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blog:login'))

    client = get_object_or_404(Client, user=request.user)

    context = {
        'client': client
    }

    return render(request, 'blog/user-update.html', context)


def upload_image(request):
    """ Upload user image NO AJAX """

    form = UserEditForm(request.POST, request.FILES)

    if form.is_valid() and request.method == 'POST' and request.FILES['image']:

        # get image and file storage
        image = form.cleaned_data['image']
        fs = FileSystemStorage()

        # get client session
        client = Client.objects.get(user=request.user)

        #filename and extension
        extension = image.name.split('.')[-1]
        filename = 'blog/profile/{}.{}'.format(client.id, 'png')
        fs.delete(filename)
        filename = fs.save(filename, image)

        client.image = '{}'.format(filename)
        client.save()

        # see uploaded file
        #fs.url(filename)

    return HttpResponseRedirect(reverse('blog:user-update'))


@require_http_methods("POST")
def create_article(request):
    """ Upload images """

    from PIL import Image

    form = ArticleForm(request.POST, request.FILES)

    if form.is_valid():

        # insert the article into db
        article = Article(client=request.user,
                          title=form.cleaned_data['title'],
                          body=form.cleaned_data['body'],
                          image=form.cleaned_data['image'])

        article.save()

        # getting article topics
        article_topics = request.POST.get('article-topics', '')
        article_topics = json.loads(article_topics)

        # add topics to article
        for key, value in article_topics.iteritems():
            topic_id = key.split('_')[-1]

            if value:
                topic = Topic.objects.get(id=topic_id)
                article.topics.add(topic)

        article.save()

        # IMAGE tasks

        # get article after inserting it
        article = Article.objects.latest('pk')

        # image article, extension and path
        image = article.image
        ext = image.name.split('.')[-1].lower()
        path = image.path

        # resize image
        image = Image.open(image)
        image = image.resize((800, 500))
        image.save('blog/static/blog/img/articles/{}.{}'.format(article.id, ext))
        article.image = 'blog/img/articles/{}.{}'.format(article.id, ext)
        article.save()

        # delete old image
        if os.path.exists(path):
            os.remove(path)

    return HttpResponseRedirect(reverse('blog:index'))


@require_http_methods("GET")
def article(request, article_id, title):
    """ Article View"""

    article_obj = get_object_or_404(Article, pk=article_id)

    comments_obj = article_obj.comment_set.all()

    context = {
        'article': article_obj,
        'comments': comments_obj
    }

    return render(request, 'blog/article.html', context)


@require_http_methods("POST")
def create_comment(request):
    """ Create comment via Ajax"""

    # check if the call is ajax
    if request.is_ajax():

        # get post values
        article_id = request.POST.get('article_id', 0)
        comment_text = request.POST.get('comment_text', '')

        # if the comment has any value
        if comment_text.strip():

            # create and save the comment
            article_obj = get_object_or_404(Article, id=article_id)
            client = get_object_or_404(Client, user=request.user)
            comment = Comment(client=client, article=article_obj, text=comment_text)
            comment.save()

            return JsonResponse({
                'comment_text': comment.text,
                'comment_username': comment.client.user.username,
                'comment_date': comment.pub_date
            })

    return HttpResponse('')


@require_http_methods(["GET", "POST"])
def ajax(request):
    """ Create comment via Ajax"""

    return Ajax(request).get_response()

