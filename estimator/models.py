import decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class RoomItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class RoomItemDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.description)[:15] + '...' + " | " + str(self.rate)


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        max_length=255, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='creator')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    reference_number = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.reference_number) + " | " + str(self.name)

    def save(self, **kwargs):
        key = not self.id
        super(Project, self).save(**kwargs)
        if key:
            self.reference_number = str(
                datetime.now().year) + '/' + str(self.pk)
            kwargs['force_insert'] = False
            super(Project, self).save(**kwargs)
        return

    def get_absolute_url(self):
        return reverse("project_expense")


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        max_length=255, blank=True, null=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(blank=True,
                                   validators=[phoneNumberRegex], max_length=11)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + ' | ' + str(self.phoneNumber)


class Estimate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_item = models.ForeignKey(RoomItem, on_delete=models.CASCADE)
    room_item_description = models.ForeignKey(
        RoomItemDescription, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.project.name) + ' | ' + str(self.room.name)
