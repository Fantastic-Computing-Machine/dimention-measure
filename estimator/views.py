from django.shortcuts import HttpResponseRedirect
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView
)
from django.views.generic.edit import FormMixin


from estimator.models import (
    Room,
    RoomItemDescription,
    RoomItem,
    Project,
    Estimate,
)
from estimator.forms import (
    NewProjectForm,
    NewEstimateItemForm,
    UpdateProjectForm,
    NewRoomForm,
    NewRoomItemForm,
    NewRoomItemDescriptionForm,
)
from client_and_company.models import CompanyDetail, Client
from client_and_company.forms import NewClientForm
from settings.models import TermsHeading, TermsContent


class AllEstimates(LoginRequiredMixin, FormMixin, ListView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    form_class = NewProjectForm
    context_object_name = 'projects_list'
    template_name = 'estimates_home.html'
    success_url = reverse_lazy('all_estimates')
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
        return HttpResponseRedirect(reverse('all_estimates'))


class UpdateEstimateProjectView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Project
    template_name = 'update_estimate_project.html'
    form_class = UpdateProjectForm


class EstimateDetailView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Estimate
    form_class = NewEstimateItemForm
    template_name = 'estimate.html'

    def get_context_data(self, **kwargs):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        estimates = Estimate.objects.filter(
            project=project, is_deleted=False).order_by('room')
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


class UpdateEstimateItemView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Estimate
    template_name = 'update_estimate_item.html'
    form_class = NewEstimateItemForm

    def post(self, request, **kwargs):
        req = request.POST
        super(UpdateEstimateItemView, self).post(request, **kwargs)
        estimate = Estimate.objects.get(pk=self.kwargs['pk'])

        estimate.room_id = req['room'][0]
        estimate.room_item_id = req['room_item'][0][0]
        estimate.room_item_description_id = req['room_item_description'][0]
        estimate.quantity = req['quantity'][0]
        estimate.unit_id = req['unit'][0]
        estimate.save()

        return HttpResponseRedirect(reverse('estimate', kwargs={"pk": self.kwargs['project_id'], "project_name": self.kwargs['project_name']}))


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


class UpdateRoomView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Room
    form_class = NewRoomForm
    template_name = 'folio/update_folio_item.html'
    success_url = reverse_lazy('folio')


class UpdateRoomItemView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = RoomItem
    form_class = NewRoomItemForm
    template_name = 'folio/update_folio_item.html'
    success_url = reverse_lazy('folio')


class UpdateRoomItemDescriptionView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = RoomItemDescription
    form_class = NewRoomItemDescriptionForm
    template_name = 'folio/update_folio_item.html'
    success_url = reverse_lazy('folio')


@login_required
def DeleteEstimate(request, pk, project_name):
    if request.method == 'POST':
        estimate = Project.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.now())
        return HttpResponseRedirect(reverse('all_estimates'))


class ClientView(LoginRequiredMixin, FormMixin, ListView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    form_class = NewClientForm
    context_object_name = 'clients_list'
    template_name = 'clients/clients.html'
    success_url = reverse_lazy("clients")
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False).order_by('-created_on')

    def post(self, request, **kwargs):
        form = NewClientForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('clients'))


class UpdateClientView(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    template_name = 'clients/update_client.html'
    form_class = NewClientForm
    success_url = reverse_lazy('clients')


@login_required
def DeleteClient(request, pk):
    if request.method == 'POST':
        client = Client.objects.filter(pk=pk).update(
            is_deleted=True, deleted_on=datetime.now())
        return HttpResponseRedirect(reverse('clients'))


@login_required
def DeleteRoom(request):
    if request.method == 'POST':
        list_to_delete = request.POST.getlist('roomCheckbox')
        for item in list_to_delete:
            room = Room.objects.filter(pk=int(item)).update(
                is_deleted=True, deleted_on=datetime.now())

        return HttpResponseRedirect(reverse('folio'))


@login_required
def DeleteRoomComponent(request):
    if request.method == 'POST':
        list_to_delete = request.POST.getlist('roomElementCheckbox')
        for item in list_to_delete:
            room_item = RoomItem.objects.filter(pk=int(item)).update(
                is_deleted=True, deleted_on=datetime.now())

        return HttpResponseRedirect(reverse('folio'))


@login_required
def DeleteComponentDescription(request):
    if request.method == 'POST':
        list_to_delete = request.POST.getlist('elementDescriptionCheckbox')
        for item in list_to_delete:
            room_item_description = RoomItemDescription.objects.filter(
                pk=int(item)).update(is_deleted=True, deleted_on=datetime.now())
        return HttpResponseRedirect(reverse('folio'))


@login_required
def AddRoom(request):
    print(request.POST)
    if request.method == 'POST':
        form = NewRoomForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('folio'))


@login_required
def AddRoomItem(request):
    if request.method == 'POST':
        form = NewRoomItemForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('folio'))


@login_required
def AddRoomItemDescription(request):
    if request.method == 'POST':
        form = NewRoomItemDescriptionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('folio'))


@login_required
def download_estimate_excel_file(request, project_id, project_name):
    date_time_obj = datetime.now()
    current_date = date_time_obj.strftime('%x')
    current_time = date_time_obj.strftime('%X')

    filename = project_name + '_' + str(current_date).replace('/', "-") + \
        '_' + str(current_time).replace(":", "-") + ".xlsx"

    file_path = "media/excel/" + filename

    project = Project.objects.filter(
        pk=project_id, is_deleted=False)[0]
    company = CompanyDetail.objects.filter(
        pk=1)[0]
    print(project)
    print(company)

    # create a workbook object
    workbook = Workbook()
    # create a worksheet
    sheet = workbook.active
    sheet.title = project_name + " Estimate"

    sheet.column_dimensions['B'].width = 70
    sheet.column_dimensions['B'].alignment = Alignment(wrapText=True)
    sheet.append(["", "Reference No.: " + str(project.reference_number),
                 "", "", "Date", current_date])
    sheet["B1"].font = Font(size=9)
    sheet["E1"].font = Font(size=9)
    sheet["F1"].font = Font(size=9)
    sheet.append([""])
    sheet.append(["", company.company_name])
    sheet["B3"].font = Font(size=12, bold=True)
    sheet.append(["", company.address()])
    sheet.append(["", "Email:"+str(company.email)])
    sheet.append(
        ["", "Mobile: " + str(company.phoneNumber) + str(company.name)])
    sheet.append([""])
    sheet.append(["", "To"])
    sheet.append(["", project.client.name])
    sheet["B9"].font = Font(size=12, bold=True)
    sheet.append(["", project.client.address()])
    sheet.append([""])
    sheet.append(["", "Estimate"])
    # sheet.append(["", project.client.address])
    sheet.append([""])
    sheet.append(["Sl.No", "Description", "Unit", "Quantity",
                  "Rate", "Amount"])
    sheet["A14"].font = Font(bold=True)
    sheet["B14"].font = Font(bold=True)
    sheet["C14"].font = Font(bold=True)
    sheet["D14"].font = Font(bold=True)
    sheet["E14"].font = Font(bold=True)
    sheet["F14"].font = Font(bold=True)
    # sheet["B14"].alignment = Alignment(wrapText=True)
    index = 1
    # room_obj = Room.objects.all()
    estimate = Estimate.objects.filter(
        project__id=project_id, is_deleted=False).order_by('room')

    print(estimate)
    print(project.get_all_rooms())

    for room_item in project.get_all_rooms():

        sheet.append([index, room_item[1]])

        estimate_room_obj = estimate.filter(room__id=room_item[0], )
        index_j = 0
        for item in estimate_room_obj:
            index_j = index_j + 1
            sheet.append([
                str(index)+"." + str(index_j),
                str(item.room_item.name) + " - " +
                str(item.room_item_description.description),
                str(item.room_item_description.unit.unit),
                str(item.quantity),
                str(item.room_item_description.rate),
                str(item.calculate_amount())
            ])
        index += 1

    sheet.append(["", "Grand Total", "", "", "", project.total_amount()])
    sheet.append(["", "GST @ 18%", "", "", "", project.gst_amount()])
    sheet.append(["", "Total including GST", "",
                 "", "", project.total_with_gst()])
    sheet.append([""])

    terms_heading_obj = TermsHeading.objects.all()

    for item in terms_heading_obj:
        sheet.append(["", item.name.upper()])
        terms_content_obj = TermsContent.objects.filter(heading__id=item.pk)

        index = 1
        for term_item in terms_content_obj:

            sheet.append([index, term_item.description])

            index += 1
        sheet.append([""])
    sheet.append([""])

    workbook.save(filename=str(file_path))
    workbook.close()
    print("WB--- CLOSE")
    file_ecxel = FileResponse(open(file_path, 'rb'))
    delete_file = os.remove(file_path)
    return file_ecxel
