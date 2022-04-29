from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class LandingView(LoginRequiredMixin, TemplateView):
    template_name = "main/dashboard.html"
