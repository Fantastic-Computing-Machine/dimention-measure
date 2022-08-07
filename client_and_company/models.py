from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

from authentication.models import Organization

from django.conf import settings
from django.contrib.auth import get_user_model as user_model
User = user_model()


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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' | ' + str(self.phoneNumber)

    def save(self):
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

    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     super().save_model(request, obj, form, change)

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
