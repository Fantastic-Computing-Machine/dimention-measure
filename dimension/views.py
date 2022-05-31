import decimal
from pymongo import MongoClient
import CONFIG
import certifi

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    ListView,
)
from django.urls import reverse_lazy, reverse
import os
import datetime
from openpyxl import Workbook
import re

from .forms import NewProjectForm, NewDimensionForm, DeleteProjectForm
from .forms import UpdateDimensionForm
from .models import Project, Dimension

from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model as user_model


User = user_model()


class HomeView(LoginRequiredMixin, FormMixin, ListView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    form_class = NewProjectForm
    context_object_name = 'projects_list'
    template_name = 'index.html'
    success_url = reverse_lazy("home")
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False).order_by('-created_on')

    # def get_context_data(self, *args, **kwargs):
    #     context = super(HomeView, self).get_context_data(*args, **kwargs)
    #     context["projects_list"] = Project.objects.filter(
    #         is_deleted=False).order_by('-created_on')
    #     return context

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('home'))


class ProjectView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Dimension
    form_class = NewDimensionForm
    template_name = 'project_detail.html'

    def get_context_data(self, *args, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        dimensions = Dimension.objects.filter(
            project=project).filter(is_deleted=False)
        kwargs['dimentions'] = dimensions
        kwargs['project'] = project
        kwargs['sum_sqm'] = sum(item.sqm for item in dimensions)
        kwargs['sum_sqft'] = sum(item.sqft for item in dimensions)
        kwargs['sum_amount'] = sum(item.amount for item in dimensions)
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


class UpdateDimensionView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
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


@login_required
def DeleteProjectView(request, pk, project_name):
    if request.method == 'POST':
        project = Project.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.datetime.now())
    return HttpResponseRedirect(reverse('home'))


@login_required
def DeleteDimensionView(request, pk, project_id, project_name):
    if request.method == 'POST':
        dimension = Dimension.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.datetime.now())
    return HttpResponseRedirect(reverse('project_detail', args=(project_id, project_name,)))


@login_required
def download_excel_view(request, project_id, project_name):
    date_time_obj = datetime.datetime.now()
    current_date = date_time_obj.strftime('%x')
    current_time = date_time_obj.strftime('%X')

    filename = project_name + '_' + str(current_date).replace('/', "-") + \
        '_' + str(current_time).replace(":", "-") + ".xlsx"

    file_path = "media/excel/" + filename

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = project_name

    sheet.append(["Project Name", project_name])
    sheet.append([""])
    sheet.append(["Tag", "Length", "Width", "Area | sqm",
                  "Area | sqft", "Rate", "Amount"])

    dimension = Dimension.objects.filter(
        project__id=project_id, is_deleted=False)

    for item in dimension:

        sheet.append([
            item.name, item.length, item.width, item.sqm, item.sqft, item.rate, item.amount
        ])

    sum_sqft = sum(item.sqft for item in dimension)
    sum_sqm = sum(item.sqm for item in dimension)
    sum_amount = sum(item.amount for item in dimension)

    sheet.append([""])
    sheet.append(['Total sqm', sum_sqm])
    sheet.append(['Total sqft', sum_sqft])
    sheet.append(['Total amount*', sum_amount])

    sheet.append([""])
    sheet.append(['*Calculated using metrics in sqft.'])

    workbook.save(filename=str(file_path))
    workbook.close()
    file_ecxel = FileResponse(open(file_path, 'rb'))
    delete_file = os.remove(file_path)
    return file_ecxel


class MongoDatabase:
    def __init__(self):
        self.databaseName = CONFIG.MONGO[0]
        self.clusterName = CONFIG.MONGO[1]
        self.connectionId = str(CONFIG.MONGO[2])

    def __connect(self):
        try:
            self.client = MongoClient(
                self.connectionId, tlsCAFile=certifi.where())
            db = self.client[self.databaseName]
            collection = db[self.clusterName]
            return collection
        except Exception as ex:
            print("MongoDB: Exception occured while Connecting to the database.")
            print(ex)
            return False

    def __disconnect(self):
        try:
            self.client = MongoClient(self.connectionId)
            self.client.close()
            return True
        except Exception as ex:
            print(
                "MongoDB: Exception occured while disconnecting to the database. \nTrying...")
            print(ex)
            return False

    def find(self, query=None, projection=None):
        # Find Many
        query_status = None
        collection = self.__connect()
        try:
            result = collection.find(query, projection)
            return result
        except Exception as ex:
            query_status = False
            print("MongoDB: Exception occured while performing Find in the database.")
            print(ex)
            return query_status
        finally:
            self.__disconnect()
            if query_status == False:
                return query_status
            return result


class MigrateData(LoginRequiredMixin, TemplateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Dimension

    def get_context_data(self, **kwargs):
        mongo_obj = MongoDatabase()
        print("\nMongo Object Created")

        user_obj = User.objects.get(username="admin")
        ct = 0

        for item in mongo_obj.find():
            projectName = item["projectName"]
            print("project Name:", projectName)

            project_obj = Project(
                name=projectName,
                author=user_obj,
            ).save()

            project_obj = Project.objects.get(name=projectName)
            ct += 1
            print(ct, ' | ', project_obj)

            cnt = 0

            for dim in range(len(item["dims"])):
                curr_dim = item["dims"][dim]

                print("Current Dimention: #", dim)

                dims_obj = Dimension(
                    project=project_obj,
                    name=curr_dim["name"],
                    length=decimal.Decimal(curr_dim["length"]),
                    width=decimal.Decimal(curr_dim["width"]),
                    rate=decimal.Decimal(curr_dim["rate"]),
                )

                dims_obj.save()

                cnt = +1
                print(cnt, ' | ', dims_obj)
            print()

        return super(MigrateData, self).get_context_data(**kwargs)
