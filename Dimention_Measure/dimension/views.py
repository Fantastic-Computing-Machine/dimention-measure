from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.forms.models import modelform_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse

import datetime
from openpyxl import Workbook
import re

from .forms import NewProjectForm, NewDimensionForm, DeleteProjectForm
from .forms import UpdateDimensionForm
from .models import Project, Dimension


class HomeView(CreateView):
    form_class = NewProjectForm
    model = Project
    success_url = reverse_lazy("home")
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["projects_list"] = Project.objects.filter(
            is_deleted=False).order_by('-created_on')
        return context

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        return super(HomeView, self).post(request, **kwargs)


class ProjectView(CreateView):
    model = Dimension
    form_class = NewDimensionForm
    template_name = 'project_detail.html'

    def get_context_data(self, *args, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        dimentions = Dimension.objects.filter(
            project=project).filter(is_deleted=False)
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
        request.POST._mutable = False
        return super(ProjectView, self).post(request, **kwargs)


class UpdateDimensionView(UpdateView):
    model = Dimension
    form_class = UpdateDimensionForm
    template_name = 'update_project.html'

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


def DeleteProjectView(request, pk, project_name):
    if request.method == 'POST':
        project = Project.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.datetime.now())
    return HttpResponseRedirect(reverse('home'))


def DeleteDimentionView(request, pk, project_id, project_name):
    if request.method == 'POST':
        dimension = Dimension.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.datetime.now())
    return HttpResponseRedirect(reverse('project_detail', args=(project_id, project_name,)))


def download_excel_view(request,project_id, project_name):
    # print(project_id, project_name)
    # date_time_obj = datetime.datetime.now()
    # current_date = date_time_obj.strftime('%x')
    # current_time = date_time_obj.strftime('%X')

    # filename = "media/excel/" + project_name + '_' + str(current_date).replace('/', "-") + \
    #     '_' + str(current_time).replace(":", "-") + ".xlsx"

    # # create a workbook object
    # workbook = Workbook()
    # # create a worksheet
    # sheet = workbook.active
    # sheet.title = project_name

    # sheet.append(["Project Name", project_name])
    # sheet.append([""])
    # sheet.append(["Tag", "Length", "Width", "Area | sqm",
    #               "Area | sqft", "Rate", "Amount"])

    # dimention = Dimension.objects.filter(project__id=project_id)
    # print(dimention)

    # for item in session['proj_info'][1]:

    #     item["length"] = str(item["length"]) + " m (" + \
    #         str(round(item["length"]*3.281, 2)) + " ft.)"
    #     item["width"] = str(item["width"]) + " m (" + \
    #         str(round(item["width"]*3.281, 2)) + " ft.)"

    #     sheet.append([item["tag"], item["length"],
    #                   item["width"], item["sqm"], item["sqft"], item["rate"], item["amount"]])

    # sheet.append([""])
    # sheet.append(['Total sqm', session['proj_info'][2]])
    # sheet.append(['Total sqft', session['proj_info'][3]])
    # sheet.append(['Total amount*', session['proj_info'][4]])

    # sheet.append([""])
    # sheet.append(['*Calculated using metrics in sqft.'])

    # print(filename)
    # workbook.save(filename=str(filename))
    # workbook.close()

    # session.pop('proj_info')
    return HttpResponseRedirect(reverse('project_detail', args=(project_id, project_name,)))

    # @ after_this_request
    # def remove_file(response):
    #     try:
    #         os.remove(filename)
    #         FileHandler.close()
    #     except Exception as error:
    #         app.logger.error(
    #             "Error removing or closing downloaded file handle", error)
    #     return response

    # return FileResponse(open(path_to_file, 'rb'), as_attachment=True)
