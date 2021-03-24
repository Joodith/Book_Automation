from django import views
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name="basepage.html"