# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
from django.db import models
from django.urls import reverse

from decimal import Decimal
from datetime import datetime


User = user_model()


def meter2feet(meters):
    # Convert meters to feet
    feet = float(meters) * 3.28084
    inches = round((feet - int(feet)) * 12, 2)
    return feet, inches


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

    length = models.DecimalField(verbose_name="Length (m)", max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    length_feet = models.IntegerField(default=0)
    length_inches = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    width = models.DecimalField(verbose_name="Width (m)", max_digits=20, decimal_places=2, blank=True, null=True)
    width_feet = models.IntegerField(blank=True, null=True,default=0)
    width_inches = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)

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
        self.description = self.description.strip()

        self.delete = datetime.now() if self.is_deleted else None

        # self.width = float(self.width) if self.width and self.width != '0' else Decimal(0)
        self.width_feet = self.width_feet if self.width_feet and self.width_feet != 0 else Decimal(0)
        self.width_inches = self.width_inches if self.width_inches and self.width_inches != 0 else Decimal(0)
        self.rate = self.rate if self.rate and self.rate != '0' else Decimal(0)

        if self.length:
            self.length_feet, self.length_inches = meter2feet(self.length)

        if self.width:
            self.width_feet, self.width_inches = meter2feet(self.width)

        # if self.length_feet or self.length_inches:
        self.length = Decimal(self.length_feet * 0.3048) + Decimal(self.length_inches * 0.0254)
        self.width = Decimal(self.width_feet * 0.3048) + Decimal(self.width_inches * 0.0254)

        if not self.width_feet or not self.width_inches:
            if self.description and '**NOTE: THIS IS RUNNING LENGTH.**' not in self.description:
                self.description = "**NOTE: THIS IS RUNNING LENGTH.** \n" + str(self.description)
            else:
                self.description = '**NOTE: THIS IS RUNNING LENGTH.**'

            self.sqm = self.length
            self.sqft = self.length * Decimal(3.28084)
            self.amount = Decimal(0) if self.rate == 0 else self.sqft * Decimal(self.rate)

        else:
            if self.description and '**NOTE: THIS IS RUNNING LENGTH.**' in self.description:
                self.description = self.description.replace('**NOTE: THIS IS RUNNING LENGTH.**', '')

            self.sqm = self.length * self.width
            self.sqft = self.length * self.width * Decimal(10.7639)
            self.amount = Decimal(0) if self.rate == 0 else self.sqft * self.rate

        return super(Dimension, self).save()

    # def calculate_sqft(self):
    #     # to calculate sqft
    #     self.sqft = self.length * self.width * Decimal(10.7639)
    #     return self.sqft

    # def calculate_sqm(self):
    #     # to calculate sqm
    #     self.sqm = self.length * self.width
    #     return self.sqm

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.project.pk), str(self.project.name)])
