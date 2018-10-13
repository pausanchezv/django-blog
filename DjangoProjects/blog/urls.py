from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

# app registration
app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^users/me/$', views.userhome, name='userhome'),
    url(r'^users/edit/$', views.user_update, name='user-update'),
    url(r'^create_article$', views.create_article, name='create_article'),
    url(r'^create_comment$', views.create_comment, name='create_comment'),
    url(r'^ajax/$', views.ajax, name='ajax'),
    url(r'^upload_image', views.upload_image, name='upload_image'),
    url(r'^(?P<article_id>[0-9]+)/(?P<title>[0-9a-zA-Z_-]+)/$', views.article, name='article')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
