from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from typing import List
import decimal
import html
import os
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from estimator.models import (
    Room,
    RoomItemDescription,
    RoomItem,
    Project,
    Estimate,
    ProjectTermsAndConditions,
)
from estimator.forms import (
    NewProjectForm,
    NewEstimateItemForm,
    UpdateProjectForm,
    NewRoomForm,
    NewRoomItemForm,
    NewRoomItemDescriptionForm,
    DiscountForm,
    UpdateProjectTermsAndConditionForm,
)
from settings.models import Unit, OrganizationTNC
from core.views import BaseAuthClass


class AllEstimates(BaseAuthClass, FormMixin, ListView):
    model = Project
    form_class = NewProjectForm
    context_object_name = "projects_list"
    template_name = "estimates_home.html"
    success_url = reverse_lazy("all_estimates")
    paginate_by = 14

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False, client__is_deleted=False).order_by(
            "-created_on"
        )

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        form = NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("all_estimates"))


class UpdateEstimateProjectView(BaseAuthClass, UpdateView):
    model = Project
    template_name = "update_estimate_project.html"
    form_class = UpdateProjectForm


class EstimateDetailView(BaseAuthClass, CreateView):
    model = Estimate
    form_class = NewEstimateItemForm
    template_name = "estimate.html"

    def get_context_data(self, **kwargs):
        project = Project.objects.filter(pk=self.kwargs["pk"])[0]
        estimates = Estimate.objects.filter(project=project, is_deleted=False).order_by(
            "room"
        )
        kwargs["project"] = project
        kwargs["units"] = Unit.objects.all()
        kwargs["all_estimates"] = estimates
        return super(EstimateDetailView, self).get_context_data(**kwargs)

    def post(self, request, **kwargs):
        active_project = Project.objects.filter(id=kwargs["pk"])[0]
        if request.method == "POST":
            request.POST._mutable = True
            request.POST["project"] = active_project
            request.POST._mutable = False
            try:
                form = NewEstimateItemForm(request.POST)
            except Exception as e:
                print(e)

        return super(EstimateDetailView, self).post(request, **kwargs)


class UpdateEstimateItemView(BaseAuthClass, UpdateView):
    model = Estimate
    template_name = "update_estimate_item.html"
    form_class = NewEstimateItemForm

    def post(self, request, **kwargs):
        req = request.POST
        super(UpdateEstimateItemView, self).post(request, **kwargs)
        estimate = Estimate.objects.get(pk=self.kwargs["pk"])

        estimate.room_id = req["room"]
        estimate.room_item_id = req["room_item"]
        estimate.room_item_description_id = req["room_item_description"]

        if req["unit"] != "":
            estimate.unit = Unit.objects.get(id=int(req["unit"]))
        else:
            estimate.unit = None

        if "quantity" in req:
            estimate.quantity = req["quantity"]
            estimate.length = None
            estimate.width = None
        else:
            estimate.length = decimal.Decimal(req["length"])
            if req["width"]:
                estimate.width = decimal.Decimal(req["width"])
            else:
                estimate.width = decimal.Decimal(0)

            estimate.quantity = None
        if "rate" in req:
            if req["rate"] == None:
                estimate.rate = decimal.Decimal(0)
            else:
                estimate.rate = decimal.Decimal(req["rate"])

        estimate.discount = req["discount"]
        estimate.save()

        return HttpResponseRedirect(
            reverse(
                "estimate",
                kwargs={
                    "pk": self.kwargs["project_id"],
                    "project_name": self.kwargs["project_name"],
                },
            )
        )


class FolioView(BaseAuthClass, CreateView):
    model = Estimate
    form_class = NewEstimateItemForm
    template_name = "folio/folio.html"

    def get_context_data(self, **kwargs):
        rooms = Room.objects.filter(is_deleted=False)
        room_item = RoomItem.objects.filter(is_deleted=False)
        room_item_description = RoomItemDescription.objects.filter(is_deleted=False)
        kwargs["units"] = Unit.objects.all()
        kwargs["rooms"] = rooms
        kwargs["room_item"] = room_item
        kwargs["room_item_description"] = room_item_description
        return super().get_context_data(**kwargs)


class UpdateRoomView(BaseAuthClass, UpdateView):
    model = Room
    form_class = NewRoomForm
    template_name = "folio/update_folio_item.html"
    success_url = reverse_lazy("folio")


class UpdateRoomItemView(LoginRequiredMixin, UpdateView):
    model = RoomItem
    form_class = NewRoomItemForm
    template_name = "folio/update_folio_item.html"
    success_url = reverse_lazy("folio")


class UpdateRoomItemDescriptionView(BaseAuthClass, UpdateView):
    model = RoomItemDescription
    form_class = NewRoomItemDescriptionForm
    template_name = "folio/update_folio_item.html"
    success_url = reverse_lazy("folio")


@login_required
def DeleteEstimate(request, pk, project_name):
    if request.method == "POST":
        estimate = Project.objects.get(pk=pk)
        estimate.is_deleted = True
        estimate.save()
        return HttpResponseRedirect(reverse("all_estimates"))


@login_required
def DeleteRoom(request):
    if request.method == "POST":
        list_to_delete = request.POST.getlist("roomCheckbox")
        for item in list_to_delete:
            room = Room.objects.get(pk=int(item))
            room.is_deleted = True
            room.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def DeleteRoomComponent(request):
    if request.method == "POST":
        list_to_delete = request.POST.getlist("roomElementCheckbox")
        for item in list_to_delete:
            room_item = RoomItem.objects.get(pk=int(item))
            room_item.is_deleted = True
            room_item.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def DeleteComponentDescription(request):
    if request.method == "POST":
        list_to_delete = request.POST.getlist("elementDescriptionCheckbox")
        for item in list_to_delete:
            room_item_description = RoomItemDescription.objects.get(pk=int(item))
            room_item_description.is_deleted = True
            room_item_description.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def AddRoom(request):
    if request.method == "POST":
        form = NewRoomForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def AddRoomItem(request):
    if request.method == "POST":
        form = NewRoomItemForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def AddRoomItemDescription(request):
    if request.method == "POST":
        form = NewRoomItemDescriptionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("folio"))


@login_required
def download_estimate_excel_file(request, project_id, project_name):
    project_tnc_obj = ProjectTermsAndConditions.objects.filter(project=project_id)
    if project_tnc_obj.count() == 0:
        return HttpResponseRedirect(
            reverse(
                "select_project_terms_and_conditions",
                kwargs={"pk": project_id, "project_name": project_name},
            )
        )

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

    project = Project.objects.filter(pk=project_id, is_deleted=False)[0]

    company = request.user.organization

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = project_name + " Estimate"

    sheet.column_dimensions["B"].width = 70
    sheet.column_dimensions["B"].alignment = Alignment(wrapText=True)
    sheet.append(
        [
            "",
            "Reference No.: " + str(project.reference_number),
            "",
            "",
            "Date",
            current_date,
        ]
    )
    sheet["B1"].font = Font(size=9)
    sheet["E1"].font = Font(size=9)
    sheet["F1"].font = Font(size=9)
    sheet.append([""])
    sheet.append(["", company.company_name.replace("-", " ").title()])
    sheet["B3"].font = Font(size=12, bold=True)
    sheet.append(["", company.address()])
    sheet.append(["", "Email: " + str(company.email)])
    sheet.append(["", "Mobile: " + str(company.phoneNumber)])
    sheet.append([""])
    sheet.append(["", "To"])
    sheet.append(["", project.client.name.replace("-", " ").title()])
    sheet["B9"].font = Font(size=12, bold=True)
    sheet.append(["", project.client.address()])
    sheet.append([""])
    sheet.append(["", "Estimate"])
    sheet["B12"].font = Font(bold=True)
    # sheet.append(["", project.client.address])
    sheet.append([""])
    sheet.append(
        ["Sl.No", "Description", "Quantity", "Unit", "Rate", "Amount", "Total"]
    )
    sheet["A14"].font = Font(bold=True)
    sheet["B14"].font = Font(bold=True)
    sheet["C14"].font = Font(bold=True)
    sheet["D14"].font = Font(bold=True)
    sheet["E14"].font = Font(bold=True)
    sheet["F14"].font = Font(bold=True)
    sheet["G14"].font = Font(bold=True)

    # sheet["B14"].alignment = Alignment(wrapText=True)
    index = 1
    # room_obj = Room.objects.all()
    estimate = Estimate.objects.filter(
        project__id=project_id, is_deleted=False
    ).order_by("room")

    for room_item in project.get_all_rooms():
        sheet.append([index, room_item[1]])

        estimate_room_obj = estimate.filter(
            room__id=room_item[0],
        )
        index_j = 0
        for item in estimate_room_obj:
            index_j = index_j + 1
            if item.unit == None:
                unit = None
            else:
                unit = item.unit.unit
            description = (
                str(item.room_item.name).replace("-", " ")
                + " - "
                + str(item.room_item_description.description).replace("-", " ").title()
            )
            if item.discount != 0:
                description = (
                    description
                    + " - "
                    + str("{:.2f}".format(item.discount) + "%")
                    + "-( Rs. "
                    + str("{:.2f}".format(item.discount_amount()))
                    + " )"
                )
            sheet.append(
                [
                    str(index) + "." + str(index_j),
                    description,
                    str(item.get_actual_quantity()),
                    str(unit),
                    str(item.rate),
                    str("{:.2f}".format(item.calculate_amount())),
                    str("{:.2f}".format(item.total_after_discount())),
                ]
            )
        index += 1

    sheet.append(
        ["", "Total itemized Discount", "", "", "", project.total_itemised_discount()]
    )
    sheet.append(["", "Grand Total", "", "", "", project.total_amount()])
    sheet.append(
        [
            "",
            "Discount ( " + str(project.discount) + "% )",
            "",
            "",
            "",
            project.discount_amount(),
        ]
    )
    sheet.append(
        ["", "Total After discount", "", "", "", project.total_after_discount()]
    )
    sheet.append(["", "GST @ 18%", "", "", "", project.gst_amount()])
    sheet.append(["", "Total including GST", "", "", "", project.total_with_gst()])
    sheet.append([""])

    for item in project_tnc_obj:
        sheet.append(["", item.heading.upper()])

        ree = re.compile("<.*?>")
        cleantext = re.sub(ree, "", item.content)

        repr_string = repr(cleantext)
        new_string = re.sub(r"\\r|\\n", "!&", repr_string)
        new_string = new_string.strip("'")
        c = new_string.split("!&!&!&!&")

        for i in c:
            sheet.append(["", html.unescape(i)])
        sheet.append([""])
    sheet.append([""])

    workbook.save(filename=str(file_path))
    workbook.close()
    with open(file_path, "rb") as excel:
        data = excel.read()

    # file_ecxel = FileResponse(open(file_path, 'rb'))
    delete_file = os.remove(file_path)
    return HttpResponse(
        data,
        headers={
            "Content-Type": "application/vnd.ms-excel",
            "Content-Disposition": 'attachment; filename= "{}"'.format(filename),
        },
    )


@login_required
def updateDiscount(request, pk, project_name):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            project = Project.objects.filter(pk=pk, is_deleted=False)[0]
            project.discount = form.cleaned_data["discount"]
            project.save()

    return HttpResponseRedirect(
        reverse(
            "estimate",
            args=(
                pk,
                project_name,
            ),
        )
    )


@login_required
def delete_estimator_item_view(request, pk, project_id, project_name):
    template_name = "delete_estimate_item.html"
    context = {}
    estimate = Estimate.objects.get(pk=pk)
    context["estimate"] = estimate

    if estimate.is_deleted:
        return HttpResponseRedirect(
            reverse(
                "estimate",
                args=(
                    project_id,
                    project_name,
                ),
            )
        )

    if request.method == "POST":
        estimate.is_deleted = True
        estimate.save()
        return HttpResponseRedirect(
            reverse(
                "estimate",
                args=(
                    project_id,
                    project_name,
                ),
            )
        )

    return render(request, template_name, context)


@login_required
def select_project_terms_and_conditions_view(request, pk: int, project_name: str):
    project_tnc = ProjectTermsAndConditions.objects.filter(project_id=pk).count()

    if int(project_tnc) != 0:
        return HttpResponseRedirect(
            reverse("project_terms_and_conditions", args=(pk, project_name))
        )

    template_name = "tnc/select_project_tnc.html"
    context = dict()
    org_tnc = OrganizationTNC.objects.filter(organization=request.user.organization)

    context["org_tnc"] = org_tnc
    context["project_name"] = project_name

    if request.method == "POST":
        to_import = list(map(int, request.POST.getlist("select_project_tnc")))
        tnc_to_import = OrganizationTNC.objects.filter(pk__in=to_import)
        project_instance = Project.objects.get(pk=pk)

        for item in tnc_to_import:
            ProjectTermsAndConditions.objects.create(
                heading=item.name,
                org_terms=item,
                project=project_instance,
                content=item.content,
            )

        return HttpResponseRedirect(
            reverse("project_terms_and_conditions", args=(pk, project_name))
        )
    return render(request, template_name, context)


@login_required
def project_terms_and_conditions_view(request, pk: int, project_name: str):
    template_name = "tnc/project_tnc.html"
    context = dict()

    project_tnc = ProjectTermsAndConditions.objects.filter(project_id=pk)
    if project_tnc.count() == 0:
        return HttpResponseRedirect(
            reverse(
                "select_project_terms_and_conditions",
                kwargs={"pk": pk, "project_name": project_name},
            )
        )
    context["project_name"] = project_name
    context["pk"] = pk
    context["project_tnc"] = project_tnc

    return render(request, template_name, context)


class UpdateProjectTermsAndCondition(BaseAuthClass, UpdateView):
    model = ProjectTermsAndConditions
    template_name = "tnc/update_project_tnc.html"
    form_class = UpdateProjectTermsAndConditionForm


@login_required
def edit_project_terms_and_conditions_list(request, pk, project_name):
    template_name = "tnc/edit_project_terms_and_conditions_list.html"
    context = dict()

    project_tnc = ProjectTermsAndConditions.objects.filter(project_id=pk)
    org_tnc = OrganizationTNC.objects.filter(organization=request.user.organization)

    project_pk = list()
    org_pk = list()

    for item in project_tnc:
        project_pk.append(int(item.org_terms.pk))

    for item in org_tnc:
        org_pk.append(int(item.pk))

    sol = list(set(org_pk) ^ set(project_pk))

    org_tnc = org_tnc.filter(pk__in=sol)

    context["org_tnc"] = org_tnc
    context["project_tnc"] = project_tnc
    context["project_name"] = project_name
    context["pk"] = pk

    if request.method == "POST":
        to_import = list(map(int, request.POST.getlist("select_project_tnc")))

        tnc_to_import = OrganizationTNC.objects.filter(pk__in=to_import)
        project_instance = Project.objects.get(pk=pk)

        for item in tnc_to_import:
            ProjectTermsAndConditions.objects.create(
                heading=item.name,
                org_terms=item,
                project=project_instance,
                content=item.content,
            )

        return HttpResponseRedirect(
            reverse("project_terms_and_conditions", args=(pk, project_name))
        )

    return render(request, template_name, context)


@login_required
def deleteSelectedProjectTnC(request, pk, project_name):
    # delete selected terms and conditions
    if request.method == "POST":
        list_to_delete = request.POST.getlist("termsAndConditionCheckBox")
        for item in list_to_delete:
            # WARNING! This is a hard delete, it will delete the item from the database
            ProjectTermsAndConditions.objects.filter(pk=item).delete()

    all_project_tnc_count = ProjectTermsAndConditions.objects.filter(
        project_id=pk
    ).count()
    if all_project_tnc_count == 0:
        return HttpResponseRedirect(
            reverse(
                "select_project_terms_and_conditions",
                kwargs={"pk": pk, "project_name": project_name},
            )
        )
    return HttpResponseRedirect(
        reverse("project_terms_and_conditions", args=(pk, project_name))
    )
