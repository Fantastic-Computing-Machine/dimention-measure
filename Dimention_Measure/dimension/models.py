from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from datetime import datetime
import decimal


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(
        max_length=255, blank=True, null=True, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author.username) + " | " + str(self.name)


class Dimension(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # length & width are in meters
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    sqm = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    # rate will be in rs/sqft
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project.name) + " | " + str(self.name)

    def save(self, *args, **kwargs):
        if self.width or self.width == 0:
            self.sqm = self.length * self.width
            self.sqft = self.length * self.width * decimal.Decimal(10.7639)
        else:
            self.sqm = self.length
            self.sqft = self.length * decimal.Decimal(3.28084)
            self.description = "**NOTE: THIS IS RUNNING LENGTH.** \n" + \
                str(self.description)

        if self.rate:
            self.amount = self.sqft * self.rate
        else:
            self.amount = null
        return super(Dimension, self).save(*args, **kwargs)


class Payee(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex], max_length=11, unique=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.phoneNumber)


PAYMENT_STATUS = [
    ("P", "Paid"),
    ("R", "Recieved"),
    ("PE", "Pending"),
    ("NA", "No Status")
]


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
