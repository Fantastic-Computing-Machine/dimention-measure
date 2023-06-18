# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
from django.db import models
from django.urls import reverse

import decimal
from datetime import datetime


User = user_model()


class Project(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            help_text="Name of the project")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who created the project")
    description = models.TextField(
        max_length=255, blank=True, null=True, help_text="Description of the project")
    created_on = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the project was created")
    is_deleted = models.BooleanField(
        default=False, help_text="Check to soft Delete the project")
    deleted_on = models.DateTimeField(
        blank=True, null=True, help_text="Date and time when the project was deleted")

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.strip().replace(" ", "-")
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        return super(Project, self).save()

    def total_amount(self):
        # to calculate total amount declared in project
        dims = Dimension.objects.filter(project=self, is_deleted=False)
        sum_amount = sum(item.amount for item in dims)
        return sum_amount

    def total_sqm(self):
        # to calculate total sqm declared in project
        dims = Dimension.objects.filter(project=self, is_deleted=False)
        sum_sqm = sum(item.sqm for item in dims)
        return sum_sqm

    def total_sqft(self):
        # to calculate total sqft declared in project
        dims = Dimension.objects.filter(project=self, is_deleted=False)
        sum_sqft = sum(item.sqft for item in dims)
        return sum_sqft

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.pk), str(self.name)])


class Dimension(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    # length & width are in meters
    length = models.DecimalField(max_digits=20, decimal_places=2)
    width = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    sqm = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    # rate will be in rs/sqft
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.project.name)

    def save(self):
        self.name = self.name.strip().replace(" ", "-")
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        if not self.width or self.width == '0' or self.width == '':
            self.width = 0

        if not self.rate or self.rate == '0' or self.rate == '':
            self.rate = 0

        if self.width == '' or self.width == 0:

            if self.description != None and self.description != '':
                if '**NOTE: THIS IS RUNNING LENGTH.**' not in self.description:
                    self.description = "**NOTE: THIS IS RUNNING LENGTH.** \n" + \
                        str(self.description)
            else:
                self.description = '**NOTE: THIS IS RUNNING LENGTH.**'

            self.sqm = self.length
            self.sqft = self.length * decimal.Decimal(3.28084)
            if self.rate == '' or self.rate == 0:
                self.amount = decimal.Decimal(0)

            elif self.rate > 0:
                self.amount = self.length * self.rate

            return super(Dimension, self).save()

        elif self.width > 0:
            if self.description != None and self.description != '':
                if '**NOTE: THIS IS RUNNING LENGTH.**' in self.description:
                    self.description = self.description.replace(
                        '**NOTE: THIS IS RUNNING LENGTH.**', '')

            self.sqm = self.length * self.width
            self.sqft = self.length * self.width * decimal.Decimal(10.7639)

            if self.rate == '' or self.rate == 0:
                self.amount = decimal.Decimal(0)

            elif self.rate > 0:
                self.amount = self.sqft * self.rate

            return super(Dimension, self).save()

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.project.pk), str(self.project.name)])
