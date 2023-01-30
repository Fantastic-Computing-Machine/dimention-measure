from datetime import datetime
import decimal

from .models import Inspection, Defect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from .forms import NewInspectionForm

from django.views.generic.edit import FormMixin
from django.shortcuts import render, HttpResponseRedirect


class BaseAuthClass(LoginRequiredMixin):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'


class InspectionHomeView(
    BaseAuthClass,
    FormMixin,
    ListView,
):
    model = Inspection
    form_class = NewInspectionForm
    context_object_name = 'inspection_list'
    template_name = 'inspection_home.html'
    success_url = reverse_lazy('inspection_home')
    paginate_by = 15

    def get_queryset(self):
        queryset = super(). get_queryset()
        return queryset.filter(is_deleted=False, inspector__organization=self.request.user.organization).order_by('-created_on')

    def post(self, request, **kwargs):
        request.POST._mutable = True
        request.POST["inspector"] = request.session["_auth_user_id"]
        request.POST._mutable = False
        form = NewInspectionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('inspection_home'))


class InspectionDetailView(BaseAuthClass, ListView):
    model = Defect
    # form_class = NewDefectForm
    template_name = 'inspection_detail.html'
    success_url = reverse_lazy('inspection_detail')

    def get_context_data(self, **kwargs):
        inspection = Inspection.objects.filter(pk=self.kwargs['pk'])[0]
        defect = Defect.objects.filter(
            project=inspection, is_deleted=False).order_by('-created_on')
        kwargs['inspection'] = inspection
        kwargs['defects'] = defect
        return super(InspectionDetailView, self).get_context_data(**kwargs)

    # def post(self, request, **kwargs):
