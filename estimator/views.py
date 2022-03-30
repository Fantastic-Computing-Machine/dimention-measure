import datetime
import re
from openpyxl import Workbook

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


from .models import *
from .forms import NewProjectForm


class AllEstimates(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    form_class = NewProjectForm
    template_name = 'all_estimates.html'

    def get_context_data(self, **kwargs):
        all_projects_object_list = Project.objects.filter(
            is_deleted=False).order_by('-created_on')
        kwargs['projects_list'] = all_projects_object_list

        return super(AllEstimates, self).get_context_data(**kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        return super(AllEstimates, self).post(request, **kwargs)


class EstimateDetailView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Estimate
    form_class = NewProjectForm
    template_name = 'estimate.html'

    def get_context_data(self, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        estimates = Estimate.objects.filter(project=project, is_deleted=False)

        kwargs['project'] = project
        kwargs['all_estimates'] = estimates

        return super(EstimateDetailView, self).get_context_data(**kwargs)
