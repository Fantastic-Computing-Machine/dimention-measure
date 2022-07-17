from ckeditor.fields import RichTextField
from settings.models import TermsHeading
import decimal
from datetime import datetime
from django.contrib.auth import get_user_model as user_model
from django.urls import reverse
from django.db import models

from client_and_company.models import Client
from settings.models import Unit

User = user_model()


class Room(models.Model):
    name = models.CharField(
        max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.replace(" ", "-").strip()
        return super(Room, self).save()


class RoomItem(models.Model):
    name = models.CharField(
        max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.replace(" ", "-").strip()
        return super(RoomItem, self).save()


class RoomItemDescription(models.Model):
    description = models.TextField(null=True)
    working = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.description)


class Project(models.Model):
    name = models.CharField(
        max_length=255)
    description = models.TextField(
        max_length=255, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='creator')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    discount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    reference_number = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.reference_number) + " | " + str(self.name)

    def save(self, **kwargs):
        self.name = self.name.replace(" ", "-").strip()
        key = not self.id
        super(Project, self).save(**kwargs)
        if key:
            self.reference_number = str(
                datetime.now().year) + '/' + str(self.pk)
            kwargs['force_insert'] = False
            super(Project, self).save(**kwargs)
        return

    def total_amount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_amount = sum(item.total_after_discount() for item in estimates)
        return sum_amount

    def total_itemised_discount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_discount = sum(item.discount_amount() for item in estimates)
        return sum_discount

    def discount_amount(self):
        return (self.total_amount() * self.discount)/100

    def total_after_discount(self):
        return self.total_amount() - self.discount_amount()

    def gst_amount(self):
        return decimal.Decimal(format(self.total_after_discount() * decimal.Decimal(0.18), ".2f"))

    def total_with_gst(self):
        return self.total_after_discount() + self.gst_amount()

    def get_all_rooms(self):
        estimate_room_obj = Estimate.objects.values_list(
            'room__id', 'room__name').filter(project__id=self.id).distinct()

        print(estimate_room_obj)

        return estimate_room_obj

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.pk), str(self.name)])


class Estimate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_item = models.ForeignKey(RoomItem, on_delete=models.CASCADE)
    room_item_description = models.ForeignKey(
        RoomItemDescription, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    sqm = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    rate = models.DecimalField(
        max_digits=20, default=0, decimal_places=2)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, null=True)
    description = models.TextField(
        max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.project.name) + ' | ' + str(self.room.name) + '|' + str(self.width)

    def save(self):
        if(self.rate == "" or self.rate == None):
            self.rate = 0.0
        if(self.unit == "" or self.unit == None):
            self.unit = None
        if(self.discount == "" or self.discount == None):
            self.discount = 0.0
        if(self.width == "" or self.width == None):
            self.width = 0.0

        if self.quantity:
            self.length = None
            self.width = None
            self.sqm = None
            self.sqft = None
            self.amount = decimal.Decimal(
                self.quantity) * self.rate
            return super(Estimate, self).save()

        else:
            if self.width == '' or self.width == 0 or self.width == 0.0:
                # when there is no width (RUNNING LENGTH)
                # SECURITY: CHECK FOR EXCEPTIONS LIKE LETTERS/SYMBOLS/NONE-TYPE/EMPTY
                if self.description != None and self.description != '':
                    if '**NOTE: THIS IS RUNNING LENGTH.**' not in self.description:
                        self.description = "**NOTE: THIS IS RUNNING LENGTH.** \n" + \
                            str(self.description)
                else:
                    self.description = '**NOTE: THIS IS RUNNING LENGTH.**'

                self.sqm = self.length
                self.sqft = self.length * decimal.Decimal(3.28084)
                self.amount = decimal.Decimal(
                    self.length) * self.rate

            elif self.width > 0:
                # AREA
                # SECURITY: CHECK FOR EXCEPTIONS LIKE LETTERS/SYMBOLS/NONE-TYPE/EMPTY
                if self.description != None and self.description != '':
                    if '**NOTE: THIS IS RUNNING LENGTH.**' in self.description:
                        self.description.replace(
                            '**NOTE: THIS IS RUNNING LENGTH.**', '')

                self.sqm = self.length * self.width
                self.sqft = self.length * self.width * decimal.Decimal(10.7639)
                self.amount = decimal.Decimal(
                    self.sqft) * self.rate

            self.quantity = None

            return super(Estimate, self).save()

    def calculate_amount(self):
        if self.quantity is not None:
            return decimal.Decimal(self.quantity) * self.rate
        return decimal.Decimal(self.sqft) * self.rate

    def discount_amount(self):
        return (self.calculate_amount() * self.discount)/100

    def total_after_discount(self):
        return self.calculate_amount() - self.discount_amount()

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.project.pk), str(self.project.name)])


class ProjectTermsAndConditions(models.Model):
    # Project TNC
    heading = models.CharField(max_length=255)
    org_terms = models.ForeignKey(TermsHeading, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = RichTextField(null=False)

    def __str__(self):
        return str(self.heading)
