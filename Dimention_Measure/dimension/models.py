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
        return str(self.name)

    def save(self):
        self.name = self.name.replace(" ", "-")
        return super(Project, self).save()

    def total_amount(self):
        dims = Dimension.objects.filter(project=self)
        sum_amount = sum(item.amount for item in dims)
        return sum_amount

    def total_sqm(self):
        dims = Dimension.objects.filter(project=self)
        sum_sqm = sum(item.sqm for item in dims)
        return sum_sqm

    def total_sqft(self):
        dims = Dimension.objects.filter(project=self)
        sum_sqft = sum(item.sqft for item in dims)
        return sum_sqft


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

    def save(self):
        self.name = self.name.replace(" ", "-")

        if self.width == '' or self.width == 0:
            self.description = "**NOTE: THIS IS RUNNING LENGTH.** \n" + \
                str(self.description)
            self.sqm = self.length
            self.sqft = self.length * decimal.Decimal(3.28084)
            if self.rate == '' or self.rate == 0:
                self.amount = decimal.Decimal(0)

            elif self.rate > 0:
                self.amount = self.length * self.rate

            return super(Dimension, self).save()

        elif self.width > 0:
            self.sqm = self.length * self.width
            self.sqft = self.length * self.width * decimal.Decimal(10.7639)

            if self.rate == '' or self.rate == 0:
                self.amount = decimal.Decimal(0)

            elif self.rate > 0:
                self.amount = self.sqft * self.rate

            return super(Dimension, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.project.pk), str(self.project.name)])
