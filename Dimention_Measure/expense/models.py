from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse

from datetime import datetime
import decimal

from dimension.models import Dimension, Project


PAYMENT_STATUS = [
    ("P", "Paid"),
    ("R", "Recieved"),
    ("PE", "Pending"),
    ("NA", "No Status")
]


class Payee(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    phoneNumber = models.CharField(blank=True,
                                   validators=[phoneNumberRegex], max_length=11)

    def __str__(self):
        return str(self.name) + " | " + str(self.phoneNumber)

    def get_absolute_url(self):
        return

    def save(self):
        self.name = self.name.replace(" ", "-")
        return super(Payee, self).save()

    def total_paid(self):
        expenses = Expense.objects.filter(
            payee=self, payment_status='P')
        total = sum(item.amount for item in expenses)
        return total

    def total_recieved(self):
        expenses = Expense.objects.filter(
            payee=self, payment_status='R')
        total = sum(item.amount for item in expenses)
        return total

    def total_pending(self):
        expenses = Expense.objects.filter(
            payee=self, payment_status='PE')
        total = sum(item.amount for item in expenses)
        return total

    def total_noStatus(self):
        expenses = Expense.objects.filter(
            payee=self, payment_status='NA')
        total = sum(item.amount for item in expenses)
        return total


class Expense(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=2,
        choices=PAYMENT_STATUS,
        default="N",
    )

    def __str__(self):
        return str(self.payee.name) + " | " + str(self.amount) + " | " + str(self.payment_status)

    def get_absolute_url(self):
        return reverse("project_expense", args=[str(self.project.pk), str(self.project.name)])
