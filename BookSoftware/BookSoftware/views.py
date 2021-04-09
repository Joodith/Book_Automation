from django import views
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


def HomeView(request):
    return HttpResponseRedirect(reverse('Account:login'))
