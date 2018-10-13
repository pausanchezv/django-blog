# -*- coding: utf-8 -*-
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from blog.models import Article, Client, Comment


class Ajax(object):
    """ Class Ajax """

    def __init__(self, request):
        """ Ajax Constructor """

        # response starts as an empty http response which will be always returned by default
        self.response = HttpResponse('')

        if request.is_ajax():

            # call the suitable handler depending on the http method
            if request.method == 'GET':
                action = request.GET.get('action', '')
                self.do_actions(request, action)

            elif request.method == 'POST':
                action = request.POST.get('action', '')
                self.do_actions(request, action)

    def get_response(self):
        """ Return the response to views.py """
        return self.response

    def do_actions(self, request, action):
        """ Handle ajax request """

        switcher = {
            'add_comment': self.add_comment,
            'index_pager': self.index_pager
        }

        try:
            switcher[action](request)
        except KeyError:
            pass
            # TODO show some error !redirect?

    def add_comment(self, request):
        """ Add comment to an article """

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

            self.response = JsonResponse({
                'comment_text': comment.text,
                'comment_username': comment.client.user.username,
                'comment_date': comment.pub_date
            })

    def index_pager(self, request):
        """ Index article paginator """

        current = int(request.GET['current'])
        quantity = int(request.GET['quantity'])

        articles = Article.objects.all()[current:current + quantity]

        response = {}

        for article in articles:

            response[article.id] = {}
            response[article.id]['id'] = article.id
            response[article.id]['title'] = article.title
            response[article.id]['username'] = article.client.username
            response[article.id]['body'] = article.body
            response[article.id]['date'] = article.pub_date
            response[article.id]['image'] = str(article.image)
            response[article.id]['topics'] = []

            for topic in article.topics.all():
                response[article.id]['topics'] += [str(topic)]




        if articles.count():
            #self.response = JsonResponse(serializers.serialize('json', articles), safe=False)

            self.response = JsonResponse(response)



