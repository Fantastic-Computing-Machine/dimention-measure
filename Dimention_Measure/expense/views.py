from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.forms.models import modelform_factory
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import re
import datetime
from .models import Payee, Expense
from .forms import NewPayeeForm, UpdatePayeeForm
from .forms import CreateExpenseForm


def total_expenses(expenses):
    context = {}
    context['total_paid'] = 0
    context['total_recieved'] = 0
    context['total_pending'] = 0
    context['total_nostatus'] = 0

    for item in expenses:
        if item.payment_status == "P":
            context['total_paid'] = context['total_paid'] + item.amount
        if item.payment_status == "R":
            context['total_recieved'] = context['total_recieved'] + item.amount
        if item.payment_status == "PE":
            context['total_pending'] = context['total_pending'] + item.amount
        if item.payment_status == "NA":
            context['total_nostatus'] = context['total_nostatus'] + item.amount

    return context


class AllExpenseView(CreateView):
    model = Payee
    template_name = 'all_expenses.html'
    form_class = NewPayeeForm
    success_url = reverse_lazy('all_expenses')

    def get_context_data(self, **kwargs):
        kwargs['payees'] = Payee.objects.all().order_by('-created_on')
        expenses = Expense.objects.all().filter(project__is_deleted=False,is_deleted=False).order_by('-created_on')
        kwargs['expenses'] = expenses
        total_expense = total_expenses(expenses)
        kwargs['total_paid'] = total_expense['total_paid']
        kwargs['total_recieved'] = total_expense['total_recieved']
        kwargs['total_pending'] = total_expense['total_pending']
        kwargs['total_nostatus'] = total_expense['total_nostatus']
        return super(AllExpenseView, self).get_context_data(**kwargs)


class PayeeExpensesView(ListView):
    model = Expense
    template_name = 'payee_expense.html'

    def get_context_data(self, **kwargs):
        kwargs['expenses'] = Expense.objects.filter(
            payee__id=self.kwargs['pk'],project__is_deleted=False,is_deleted=False).order_by('-created_on')
        kwargs['payee'] = Payee.objects.filter(
            id=self.kwargs['pk'])[0]
        return super(PayeeExpensesView, self).get_context_data(**kwargs)


class UpdatePayeeView(UpdateView):
    model = Payee
    template_name = 'update_payee.html'
    form_class = UpdatePayeeForm
    success_url = reverse_lazy('home')


# def ProjectExpenseViews(request, project_id, project_name):
#     context = {}
#     payees = Payee.objects.all().order_by('-created_on')
#     expenses = Expense.objects.filter(
#         project__id=project_id).order_by('-created_on')
#     context['payees'] = payees
#     context['project_name'] = project_name
#     context['project_id'] = project_id
#     context['expenses'] = expenses

#     total_expense = total_expenses(expenses)

#     print(total_expense)
#     context['total_paid'] = total_expense['total_paid']
#     context['total_recieved'] = total_expense['total_recieved']
#     context['total_pending'] = total_expense['total_pending']
#     context['total_nostatus'] = total_expense['total_nostatus']

#     if request.method == 'POST':
#         return

#     return render(request, 'project_expense.html', context)


class ProjectExpenseView(CreateView):
    model = Expense
    form_class = CreateExpenseForm
    template_name = 'project_expense.html'

    def get_context_data(self, **kwargs):
        payees = Payee.objects.filter(expense__project__id=self.kwargs['project_id'],expense__is_deleted=False).order_by('-created_on').distinct()
        expenses = Expense.objects.filter(
            project__id=self.kwargs['project_id'],is_deleted=False).order_by('-created_on')
        kwargs['payees'] = payees
        kwargs['project_name'] = self.kwargs['project_name']
        kwargs['project_id'] = self.kwargs['project_id']
        kwargs['expenses'] = expenses

        total_expense = total_expenses(expenses)

        kwargs['total_paid'] = total_expense['total_paid']
        kwargs['total_recieved'] = total_expense['total_recieved']
        kwargs['total_pending'] = total_expense['total_pending']
        kwargs['total_nostatus'] = total_expense['total_nostatus']

        return super(ProjectExpenseView, self).get_context_data(**kwargs)

    def post(self, request, **kwargs):
        if request.POST.get('new_expense'):
            request.POST._mutable = True
            request.POST["project"] = self.kwargs['project_id']
            request.POST._mutable = False

        if request.POST.get('new_payee'):
            form = NewPayeeForm(request.POST)
            if form.is_valid():
                form.save()

        return super(ProjectExpenseView, self).post(request, **kwargs)

def DeletePayeeView(request, payee_id,project_id,project_name):
    if request.method == 'POST':
        expense = Expense.objects.filter(project__id=project_id,payee__id=payee_id).update(is_deleted=True,deleted_on=datetime.datetime.now())
        return HttpResponseRedirect(reverse('project_expense', kwargs={'project_id': project_id,'project_name':project_name,}))