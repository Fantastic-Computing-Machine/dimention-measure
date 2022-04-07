import datetime
import re
from openpyxl import Workbook

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


from .models import *
from .forms import NewProjectForm, NewEstimateItemForm, NewClientForm, UpdateProjectForm


class AllEstimates(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    form_class = NewProjectForm
    template_name = 'estimates_home.html'

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
    form_class = NewEstimateItemForm
    template_name = 'estimate.html'

    def get_context_data(self, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        estimates = Estimate.objects.filter(project=project, is_deleted=False)
        kwargs['project'] = project
        kwargs['all_estimates'] = estimates
        return super(EstimateDetailView, self).get_context_data(**kwargs)

    def post(self, request, **kwargs):
        active_project = Project.objects.filter(id=kwargs['pk'])[0]

        if request.method == 'POST':
            request.POST._mutable = True
            request.POST["project"] = active_project
            request.POST._mutable = False
        return super(EstimateDetailView, self).post(request, **kwargs)


class UpdateEstimateProjectView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    template_name = 'update_estimate_project.html'
    form_class = UpdateProjectForm


class FolioView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Estimate
    form_class = NewEstimateItemForm
    template_name = 'folio/folio.html'

    def get_context_data(self, **kwargs):
        rooms = Room.objects.filter(is_deleted=False)
        room_item = RoomItem.objects.filter(is_deleted=False)
        room_item_description = RoomItemDescription.objects.filter(
            is_deleted=False)
        kwargs['rooms'] = rooms
        kwargs['room_item'] = room_item
        kwargs['room_item_description'] = room_item_description
        return super().get_context_data(**kwargs)


class ClientView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    template_name = 'clients/clients.html'
    form_class = NewClientForm

    def get_context_data(self, **kwargs):
        all_clients_object_list = Client.objects.filter(
            is_deleted=False).order_by('-created_on')
        kwargs['clients_list'] = all_clients_object_list

        return super(ClientView, self).get_context_data(**kwargs)


class UpdateClientView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    template_name = 'clients/update_client.html'
    form_class = NewClientForm
    success_url = reverse_lazy('clients')
