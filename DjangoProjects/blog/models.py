# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import uuid4

from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.
from django.utils import timezone

from blog.utils import Utils
from django.db.models.signals import post_save


class Client(models.Model):
    """ Website client"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField('Image',
                              upload_to='profile',
                              default='blog/profile/no_image.png')

    def __str__(self):
        return u'{}'.format(self.user.username)

    def __unicode__(self):
        return u'{}'.format(self.user.username)


def create_client(sender, **kwargs):
    if kwargs['created']:
        Client.objects.create(user=kwargs['instance'])


post_save.connect(create_client, sender=User)


class Topic(models.Model):
    """ Class Topic """

    name = models.CharField('Name', max_length=30)

    def __str__(self):
        return u'{}'.format(self.name)

    def __unicode__(self):
        return u'{}'.format(self.name)


def rename_image_article_images(obj, filename):
    """ Rename image and path """

    upload_to = 'blog/static/blog/img/articles'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext.lower())

    return os.path.join(upload_to, filename)


class Article(models.Model):
    """ Article model """

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=100)
    pub_date = models.DateTimeField('Date Published', default=datetime.now)
    body = models.TextField('Body')
    image = models.ImageField('Image',
                              upload_to=rename_image_article_images,
                              default='blog/static/blog/img/articles/no_image.png')

    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return u'{}'.format(self.title)

    def __unicode__(self):
        return u'{}'.format(self.title)


class Comment(models.Model):
    """ Class Comment """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None)
    pub_date = models.DateTimeField('Date Published', default=timezone.now)
    text = models.TextField('Text')

    def __str__(self):
        return u'{}'.format(self.text[0:20])

    def __unicode__(self):
        return u'{}'.format(self.text[0:20])


class Like(models.Model):
    """ Class Like """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)
    value = models.BooleanField('Value')


    def __str__(self):
        return u'{} - {} - {}'.format(self.id, self.client, self.value)

    def __unicode__(self):
        return u'{} - {} - {}'.format(self.id, self.client, self.value)




