from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView,
    ListView,
)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse

import decimal
import os
from datetime import datetime
from openpyxl import Workbook
import re
from decimal import Decimal
from .forms import (
    NewProjectForm,
    UpdateProjectForm,
    NewDimensionForm,
    UpdateDimensionForm,
)
from django.contrib import messages

# from .forms import
from .models import Project, Dimension
from core.views import BaseAuthClass

User = user_model()


# Caching of static files such as css, js, images
# Like this:
# [18/Nov/2023 12:38:07] "GET /assets/css/styles.css HTTP/1.1" 200 4385
# [18/Nov/2023 12:38:07] "GET /assets/img/iconGrey.svg HTTP/1.1" 200 1161
# [18/Nov/2023 12:38:07] "GET /assets/js/main.js HTTP/1.1" 200 8719
# [18/Nov/2023 12:38:07] "GET /assets/img/favicon.ico HTTP/1.1" 200 216542


class DimensionHomeView(BaseAuthClass, FormMixin, ListView):
    """Class view for dimension home page"""

    # Note: Choosing List view because I have to use Pagination.

    model = Project
    form_class = NewProjectForm
    context_object_name = "projects_list"
    template_name = "dimensions_home.html"
    success_url = reverse_lazy("home")
    paginate_by = 14
    context = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            is_deleted=False, author__organization=self.request.user.organization
        ).order_by("-created_on")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        form = NewProjectForm(request.POST)
        # TODO: Check if project name exists and return error
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("home"))


class DimensionProjectView(BaseAuthClass, CreateView):
    """Class view for dimension project page"""

    model = Dimension
    form_class = NewDimensionForm
    template_name = "project_detail.html"

    def get_context_data(self, *args, **kwargs):
        project = Project.objects.filter(pk=self.kwargs["pk"])[0]
        dimensions = Dimension.objects.filter(project=project).filter(is_deleted=False)
        kwargs["dimentions"] = dimensions
        kwargs["project"] = project
        return super(DimensionProjectView, self).get_context_data(*args, **kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["width_feet"] = request.POST.get("width_feet", "0.0")
        request.POST["width_inches"] = request.POST.get("width_inches", "0.0")
        request.POST["rate"] = request.POST.get("rate", "0.0")

        request.POST["project"] = str(kwargs["pk"])
        request.POST._mutable = False
        return super(DimensionProjectView, self).post(request, **kwargs)


class UpdateProjectView(BaseAuthClass, UpdateView):
    """Class view for updating project"""

    model = Project
    form_class = UpdateProjectForm
    template_name = "update_dimension_project.html"

    def form_valid(self, form):
        # Check if project name exists
        project_name = form.cleaned_data["name"]
        if (
            Project.objects.filter(name=project_name).exists()
            and project_name != self.object.name
        ):
            form.add_error("name", "A project with this name already exists.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        return response


class UpdateDimensionView(BaseAuthClass, UpdateView):
    """Class view for updating dimension"""

    model = Dimension
    form_class = UpdateDimensionForm
    template_name = "update_item.html"

    def get_context_data(self, *args, **kwargs):
        dimension = Dimension.objects.filter(pk=self.kwargs["pk"])[0]
        kwargs["dimension"] = dimension
        return super(UpdateDimensionView, self).get_context_data(*args, **kwargs)

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["width_feet"] = request.POST.get("width_feet", "0") or "0"
        request.POST["width_inches"] = request.POST.get("width_inches", "0") or "0"
        request.POST["rate"] = request.POST.get("rate", "0") or "0"
        request.POST["project"] = str(kwargs["pk"])
        request.POST._mutable = False
        return super(UpdateDimensionView, self).post(request, **kwargs)


@login_required
def DeleteProjectView(request, pk, project_name):
    """Function view for soft deleting Entire project"""
    if request.method == "POST":
        project = Project.objects.get(pk=pk)
        project.is_deleted = True
        project.save()
        return HttpResponseRedirect(reverse("home"))

    template_name = "delete_project.html"
    context = {}
    project = Project.objects.filter(pk=pk)[0]
    context["project"] = project

    if project.is_deleted:
        return HttpResponseRedirect(reverse("home"))

    return render(request, template_name, context)


@login_required
def DeleteDimensionView(request, pk, project_id, project_name):
    # Function view for soft deleting dimension
    template_name = "delete_item.html"
    context = {}
    dimension = Dimension.objects.get(pk=pk)
    context["dimension"] = dimension

    if dimension.is_deleted:
        return HttpResponseRedirect(
            reverse(
                "project_detail",
                args=(
                    project_id,
                    project_name,
                ),
            )
        )

    if request.method == "POST":
        dimension.is_deleted = True
        dimension.save()
        return HttpResponseRedirect(
            reverse(
                "project_detail",
                args=(
                    project_id,
                    project_name,
                ),
            )
        )

    return render(request, template_name, context)


@login_required
def download_excel_view(request, project_id, project_name):
    # Function view for downloading excel file

    date_time_obj = datetime.now()
    current_date = date_time_obj.strftime("%x")
    current_time = date_time_obj.strftime("%X")

    file_name = project_name
    if len(file_name) > 17:
        file_name = file_name[:17]

    filename = (
        file_name
        + "_"
        + str(current_date).replace("/", "")
        + str(current_time).replace(":", "")
        + ".xlsx"
    )

    file_path = "media/excel/" + filename

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = project_name

    sheet.append(["Project Name", project_name])
    sheet.append([""])
    sheet.append(
        [
            "S.No.",
            "Tag",
            "Length",
            "Width",
            "Area | sqm",
            "Area | sqft",
            "Rate",
            "Amount",
        ]
    )

    dimension = Dimension.objects.filter(project__id=project_id, is_deleted=False)

    sno = 1

    for item in dimension:
        sheet.append(
            [
                str(sno),
                item.name,
                f"{str(float(item.length_feet))}' {str(float(item.length_inches))}\"",
                f"{str(float(item.width_feet))}'{str(float(item.width_inches))}\"",
                str(item.sqm),
                str(item.sqft),
                str(item.rate),
                str(item.amount),
            ]
        )
        sheet.append(["", item.description])
        sno += 1

    sum_sqft = sum(item.sqft for item in dimension)
    sum_sqm = sum(item.sqm for item in dimension)
    sum_amount = sum(item.amount for item in dimension)

    sheet.append([""])
    sheet.append(["Total sqm", float(sum_sqm)])
    sheet.append(["Total sqft", float(sum_sqft)])
    sheet.append(["Total amount*", float(sum_amount)])

    sheet.append([""])
    sheet.append(["*Calculated using metrics in sqft."])

    workbook.save(filename=str(file_path))
    workbook.close()
    file_ecxel = FileResponse(open(file_path, "rb"))
    delete_file = os.remove(file_path)
    return file_ecxel

class CheckProjectNameView(BaseAuthClass, APIView):
    """Class view for checking if project name exists"""
    def get(self, request, *args, **kwargs):
        #check project name if already exists
        project_name = request.GET.get('name', None)
        data = {
            'is_taken': Project.objects.filter(name__iexact=project_name).exists()
        }
        return JsonResponse(data)