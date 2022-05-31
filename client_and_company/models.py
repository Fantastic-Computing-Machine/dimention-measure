from tabnanny import verbose
from django_countries.fields import CountryField
import decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db import models

from authentication.models import Organization

from django.conf import settings


class Client(models.Model):
    name = models.CharField(
        max_length=255)
    description = models.TextField(
        max_length=255, blank=True, null=True)

    phoneNumber = models.CharField(blank=True,
                                   validators=[settings.PHONE_NUMBER_FORMAT], max_length=11)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    address_1 = models.CharField(max_length=255, default="abc")
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    state = models.CharField(choices=settings.STATE_CHOICES,
                             max_length=255, default='abc')
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.name) + ' | ' + str(self.phoneNumber)

    def save(self, request, obj):
        print(request)
        print(obj)
        self.name = self.name.replace(" ", "-").strip().lower()
        if self.description:
            self.description = self.description.strip()
        self.address_1 = self.address_1.strip()
        if self.address_2:
            self.address_2 = self.address_2.strip()
        if self.landmark:
            self.landmark = self.landmark.strip()
        self.town_city = self.town_city.strip()
        return super(Client, self).save()

    def address(self):
        full_address = self.address_1
        if self.address_2:
            full_address = full_address + ", " + self.address_2
        if self.landmark:
            full_address = full_address + ", " + self.landmark
        full_address = full_address + ", " + self.town_city + \
            ", " + self.state + " - " + self.zip_code
        return full_address

    def get_absolute_url(self):
        return reverse("clients")
