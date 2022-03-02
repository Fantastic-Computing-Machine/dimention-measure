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
)
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import re

from .models import Payee, Expense
from .forms import NewPayeeForm


class AllExpenseView(CreateView):
    model = Payee
    template_name = 'all_expenses.html'
    form_class = NewPayeeForm
    success_url = reverse_lazy('all_expenses')

    def get_context_data(self, **kwargs):
        kwargs['payees'] = Payee.objects.all()
        expenses = Expense.objects.all().order_by('-created_on')
        kwargs['expenses'] = expenses

        # kwargs['total_paid'] = total = sum(
        #     item.amount for item in expenses.filter(payment_status="P"))
        total_paid = 0
        total_recieved = 0
        total_pending = 0
        total_nostatus = 0

        for item in kwargs['expenses']:
            if item.payment_status == "P":
                total_paid = total_paid + item.amount
            if item.payment_status == "R":
                total_recieved = total_recieved + item.amount
            if item.payment_status == "PE":
                total_pending = total_pending + item.amount
            if item.payment_status == "NA":
                total_nostatus = total_nostatus + item.amount

        kwargs['total_paid'] = total_paid
        kwargs['total_recieved'] = total_recieved
        kwargs['total_pending'] = total_pending
        kwargs['total_nostatus'] = total_nostatus
        return super(AllExpenseView, self).get_context_data(**kwargs)


class PayeeExpensesView(ListView):
    model = Expense
    template_name = 'payee_expense.html'

    def get_context_data(self, **kwargs):
        kwargs['expenses'] = Expense.objects.filter(
            payee__id=self.kwargs['pk'])
        kwargs['payee'] = Payee.objects.filter(
            id=self.kwargs['pk'])[0]
        # print(payee)
        # kwargs['expenses'] = expenses
        return super(PayeeExpensesView, self).get_context_data(**kwargs)
