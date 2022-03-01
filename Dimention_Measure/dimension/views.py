from django.forms.models import modelform_factory
from django.db.models import Q, F
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import re

from .forms import NewProjectForm, NewDimensionForm
from .forms import UpdateDimensionForm
from .models import Project, Dimension


class HomeView(CreateView):
    form_class = NewProjectForm
    model = Project
    success_url = reverse_lazy("home")
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["projects_list"] = Project.objects.order_by('-created_on')
        return context

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        print("PINN: ", request.POST)
        return super(HomeView, self).post(request, **kwargs)


class ProjectView(CreateView):
    model = Dimension
    form_class = NewDimensionForm
    template_name = 'dimensions/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        print(project)
        dimentions = Dimension.objects.filter(project=project)
        kwargs['dimentions'] = dimentions
        kwargs['project'] = project
        kwargs['sum_sqm'] = sum(item.sqm for item in dimentions)
        kwargs['sum_sqft'] = sum(item.sqft for item in dimentions)
        kwargs['sum_amount'] = sum(item.amount for item in dimentions)
        return super(ProjectView, self).get_context_data(*args, **kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        if request.POST['width'] == '':
            request.POST['width'] = '0'
        if request.POST['rate'] == '':
            request.POST['rate'] = '0'
        request.POST["project"] = str(kwargs['pk'])
        request.POST._mutable = True
        return super(ProjectView, self).post(request, **kwargs)


class UpdateDimensionView(UpdateView):
    model = Dimension
    form_class = UpdateDimensionForm
    template_name = 'dimensions/update_project.html'

    def get_context_data(self, *args, **kwargs):
        dimension = Dimension.objects.filter(pk=self.kwargs['pk'])[0]
        kwargs['dimension'] = dimension
        return super(UpdateDimensionView, self).get_context_data(*args, **kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        if request.POST['width'] == '':
            request.POST['width'] = '0'
        if request.POST['rate'] == '':
            request.POST['rate'] = '0'
        request.POST["project"] = str(kwargs['pk'])
        request.POST._mutable = True
        return super(UpdateDimensionView, self).post(request, **kwargs)


class DeleteDimentionView(DeleteView):
    pass


class DeleteProjectView(DeleteView):
    success_url = reverse_lazy("home")
    pass
