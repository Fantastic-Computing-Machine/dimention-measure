
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
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseAuthClass(LoginRequiredMixin):
    # Class to be inherited by all views that require login
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'


class DashboardView(BaseAuthClass, TemplateView):
    """
    Class view for dashboard page
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['dimensions'] = DimensionProject.objects.filter(
            is_deleted=False).order_by('-created_on')[:5]
        kwargs['estimates'] = EstimateProject.objects.filter(
            is_deleted=False).order_by('-created_on')[:5]
        return super().get_context_data(**kwargs)

# search class based view


class SearchView(BaseAuthClass, APIView):
    """
    Class view for search page
    """

    def post(self, request, format=None):
        if (request.data.get('type') == 'dimension'):
            dimensions = DimensionProject.objects.filter(
                is_deleted=False, name__icontains=request.data['textToSearch'])
            results = []
            for dimension in dimensions:
                results_item = dict()
                results_item["title"] = dimension.name.capitalize()
                results_item["url"] = reverse('project_detail', args=[
                                              str(dimension.pk), str(dimension.name)])
                results_item["created_on"] = dimension.created_on.date()

                results.append(results_item)

            return Response({'success': True, 'results': results})
        elif (request.data.get('type') == 'estimate'):
            estimates = EstimateProject.objects.filter(
                is_deleted=False, name__icontains=request.data['textToSearch'])
            results = []
            for estimate in estimates:
                results_item = dict()
                results_item["title"] = estimate.name.capitalize()
                results_item["url"] = reverse(
                    'estimate', args=[str(estimate.pk), str(estimate.name)])
                results_item["created_on"] = estimate.created_on.date()

                results.append(results_item)
            return Response({'success': True, 'results': results})
        return Response({'success': False, 'results': []})
