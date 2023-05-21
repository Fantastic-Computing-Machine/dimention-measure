from django.shortcuts import render
import decimal
# from pymongo import MongoClient
# from database import MONGO
# import certifi

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView,
    ListView,
)
from django.urls import reverse_lazy, reverse
import os
from datetime import datetime
from openpyxl import Workbook
import re

from .forms import NewProjectForm, NewDimensionForm
from .forms import UpdateDimensionForm
from .models import Project, Dimension

from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model as user_model


User = user_model()


class BaseAuthClass(LoginRequiredMixin):
    # Class to be inherited by all views that require login
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'


class DimensionHomeView(BaseAuthClass, FormMixin, ListView):
    # Class view for dimension home page
    model = Project
    form_class = NewProjectForm
    context_object_name = 'projects_list'
    template_name = 'dimensions_home.html'
    success_url = reverse_lazy("home")
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False).order_by('-created_on')

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('home'))


class DimensionProjectView(BaseAuthClass, CreateView):
    # Class view for dimension project page
    model = Dimension
    form_class = NewDimensionForm
    template_name = 'project_detail.html'

    def get_context_data(self, *args, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        dimensions = Dimension.objects.filter(
            project=project).filter(is_deleted=False)
        kwargs['dimentions'] = dimensions
        kwargs['project'] = project
        return super(DimensionProjectView, self).get_context_data(*args, **kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        if request.POST['width'] == '':
            request.POST['width'] = '0'
        if request.POST['rate'] == '':
            request.POST['rate'] = '0'
        request.POST["project"] = str(kwargs['pk'])
        request.POST._mutable = False
        return super(DimensionProjectView, self).post(request, **kwargs)


class UpdateDimensionView(BaseAuthClass, UpdateView):
    # Class view for updating dimension
    model = Dimension
    form_class = UpdateDimensionForm
    template_name = 'update_item.html'

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
        request.POST._mutable = False
        return super(UpdateDimensionView, self).post(request, **kwargs)


@login_required
def DeleteProjectView(request, pk, project_name):
    # Function view for soft deleting Entire project
    if request.method == 'POST':
        project = Project.objects.get(pk=pk)
        project.is_deleted = True
        project.save()
        return HttpResponseRedirect(reverse('home'))

    template_name = "delete_project.html"
    context = {}
    project = Project.objects.filter(pk=pk)[0]
    context['project'] = project

    if project.is_deleted:
        return HttpResponseRedirect(reverse('home'))

    return render(request, template_name, context)


@login_required
def DeleteDimensionView(request, pk, project_id, project_name):
    # Function view for soft deleting dimension
    template_name = "delete_item.html"
    context = {}
    dimension = Dimension.objects.get(pk=pk)
    context['dimension'] = dimension

    if dimension.is_deleted:
        return HttpResponseRedirect(reverse('project_detail', args=(project_id, project_name,)))

    if request.method == 'POST':
        dimension.is_deleted = True
        dimension.save()
        return HttpResponseRedirect(reverse('project_detail', args=(project_id, project_name,)))

    return render(request, template_name, context)


@login_required
def download_excel_view(request, project_id, project_name):
    # Function view for downloading excel file

    date_time_obj = datetime.now()
    current_date = date_time_obj.strftime('%x')
    current_time = date_time_obj.strftime('%X')

    file_name = project_name
    if len(file_name) > 17:
        file_name = file_name[:17]

    filename = file_name + '_' + \
        str(current_date).replace('/', "") + \
        str(current_time).replace(":", "") + ".xlsx"

    file_path = "media/excel/" + filename

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = project_name

    sheet.append(["Project Name", project_name])
    sheet.append([""])
    sheet.append(["S.No.", "Tag", "Length", "Width", "Area | sqm",
                  "Area | sqft", "Rate", "Amount"])

    dimension = Dimension.objects.filter(
        project__id=project_id, is_deleted=False)

    sno = 1

    for item in dimension:

        sheet.append([
            str(sno), item.name, str(item.length), str(
                item.width), str(item.sqm), str(item.sqft), str(item.rate), str(item.amount)
        ])
        sheet.append(["", item.description])
        sno += 1

    sum_sqft = sum(item.sqft for item in dimension)
    sum_sqm = sum(item.sqm for item in dimension)
    sum_amount = sum(item.amount for item in dimension)

    sheet.append([""])
    sheet.append(['Total sqm', float(sum_sqm)])
    sheet.append(['Total sqft', float(sum_sqft)])
    sheet.append(['Total amount*', float(sum_amount)])

    sheet.append([""])
    sheet.append(['*Calculated using metrics in sqft.'])

    workbook.save(filename=str(file_path))
    workbook.close()
    file_ecxel = FileResponse(open(file_path, 'rb'))
    delete_file = os.remove(file_path)
    return file_ecxel
