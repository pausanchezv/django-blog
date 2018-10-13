from django.http import HttpResponseRedirect
from django.urls import reverse


def index_redirect(request):
    return HttpResponseRedirect(reverse('blog:index'))
