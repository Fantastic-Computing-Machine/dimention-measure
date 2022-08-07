from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView
)
from django.views.generic.edit import FormMixin
from django.shortcuts import HttpResponseRedirect

from client_and_company.models import Client
from client_and_company.forms import NewClientForm


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
        request.POST._mutable = True
        request.POST["created_by"] = request.session["_auth_user_id"]
        request.POST["organization"] = str(request.user.organization.id)
        request.POST._mutable = False
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
