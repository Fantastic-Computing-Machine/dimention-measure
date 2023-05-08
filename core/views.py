
from dimension.models import Dimension, Project as DimensionProject
from estimator.models import Estimate, Project as EstimateProject


from datetime import datetime

from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['dimensions'] = DimensionProject.objects.filter(is_deleted=False).order_by('-created_on')[:6]
        kwargs['estimates'] = EstimateProject.objects.filter(is_deleted=False).order_by('-created_on')[:6]
        return super().get_context_data(**kwargs)