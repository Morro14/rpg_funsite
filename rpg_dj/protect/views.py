from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PersonalPageView(TemplateView, LoginRequiredMixin):
    template_name = 'protect/personal_page.html'
