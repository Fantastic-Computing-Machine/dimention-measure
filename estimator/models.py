from ckeditor.fields import RichTextField
from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model as user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from client_and_company.models import Client
from django.utils.translation import gettext as _
from settings.models import OrganizationTNC, Unit

User = user_model()

zero2hundred = [MinValueValidator(0), MaxValueValidator(100)]


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.replace(" ", "-").strip()
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        return super(Room, self).save()


class RoomItem(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.replace(" ", "-").strip()
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        return super(RoomItem, self).save()


class RoomItemDescription(models.Model):
    description = models.TextField(null=True)
    working = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.description)

    def save(self):
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        return super(RoomItemDescription, self).save()


class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    discount = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        validators=zero2hundred,
    )
    reference_number = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return str(self.reference_number) + " | " + str(self.name)

    def save(self, **kwargs):
        self.name = self.name.replace(" ", "-").strip()
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        key = not self.id
        super(Project, self).save(**kwargs)
        if key:
            self.reference_number = str(datetime.now().year) + "/" + str(self.pk)
            kwargs["force_insert"] = False
            super(Project, self).save(**kwargs)
        return

    def total_amount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_amount = sum(item.total_after_discount() for item in estimates)
        return sum_amount

    def total_itemized_discount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_discount = sum(item.discount_amount() for item in estimates)
        return sum_discount

    def discount_amount(self):
        return (self.total_amount() * self.discount) / 100

    def total_after_discount(self):
        return self.total_amount() - self.discount_amount()

    def gst_amount(self):
        return Decimal(format(self.total_after_discount() * Decimal(0.18), ".2f"))

    def total_with_gst(self):
        return self.total_after_discount() + self.gst_amount()

    def get_all_rooms(self):
        estimate_room_obj = (
            Estimate.objects.values_list("room__id", "room__name")
            .filter(project__id=self.id)
            .distinct()
        )

        return estimate_room_obj

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.pk), str(self.name)])


class Estimate(models.Model):
    """Estimate Model
    Lengths and Widths are in metric units
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_item = models.ForeignKey(RoomItem, on_delete=models.CASCADE)
    room_item_description = models.ForeignKey(
        RoomItemDescription, on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True
    )
    length = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sqm = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sqft = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        validators=zero2hundred,
    )
    rate = models.DecimalField(max_digits=20, decimal_places=5)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.project.name) + " | " + str(self.room.name)

    # def save(self):
    #     if not self.rate:
    #         self.rate = Decimal(0)
    #     if not self.unit:
    #         self.unit = None
    #     if not self.discount:
    #         self.discount = Decimal(0)
    #     if not self.width:
    #         self.width = Decimal(0)
    #     if self.is_deleted:
    #         self.deleted_on = datetime.now()
    #     if not self.is_deleted:
    #         self.deleted_on = None

    #     if self.quantity:
    #         self.length = None
    #         self.width = None
    #         self.sqm = None
    #         self.sqft = None
    #         self.amount = Decimal(self.quantity) * Decimal(self.rate)
    #         return super(Estimate, self).save()

    #     else:
    #         if self.length and (
    #             self.width == "" or self.width == 0 or self.width == 0.0
    #         ):
    #             # when there is no width (RUNNING LENGTH)
    #             # SECURITY: CHECK FOR EXCEPTIONS LIKE LETTERS/SYMBOLS/NONE-TYPE/EMPTY

    #             self.sqm = self.length
    #             self.sqft = Decimal(self.length) * Decimal(3.28084)
    #             self.amount = Decimal(self.length) * Decimal(self.rate)

    #         elif self.width and self.length:
    #             # AREA
    #             # SECURITY: CHECK FOR EXCEPTIONS LIKE LETTERS/SYMBOLS/NONE-TYPE/EMPTY

    #             self.sqm = Decimal(self.length) * Decimal(self.width)
    #             self.sqft = (
    #                 Decimal(self.length) * Decimal(self.width) * Decimal(10.7639)
    #             )
    #             self.amount = Decimal(self.sqft) * Decimal(self.rate)

    #         self.quantity = None
    #         return super(Estimate, self).save()

    def save(self):
        """Business Logic: Save and compute for the estimate"""
        if not self.rate:
            self.rate = Decimal(0)
        if not self.unit:
            self.unit = None
        if not self.discount:
            self.discount = Decimal(0)
        if not self.width:
            self.width = Decimal(0)
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None

        if self.width and (isinstance(self.width, float), isinstance(self.width, int)):
            self.width = Decimal(self.width)
            self.compute_for_area()

        elif self.quantity and (
            isinstance(self.quantity, float),
            isinstance(self.quantity, int),
        ):
            self.quantity = Decimal(self.quantity)
            self.compute_for_quantity()

        else:
            self.width = None
            self.compute_for_rft()

    def compute_for_area(self):
        """Set area of the estimate"""
        if self.width and self.length:
            self.sqm = Decimal(self.length) * Decimal(self.width)
            self.sqft = Decimal(self.length) * Decimal(self.width) * Decimal(10.7639)
            self.amount = Decimal(self.sqft) * Decimal(self.rate)

    def compute_for_rft(self):
        """Compute for Running Feet"""
        if self.length:
            self.sqm = self.length
            self.sqft = Decimal(self.length) * Decimal(3.28084)
            self.amount = Decimal(self.length) * Decimal(self.rate)

    def compute_for_quantity(self):
        """Compute for Quantity"""
        if self.quantity:
            self.length = None
            self.width = None
            self.sqm = None
            self.sqft = None
            self.amount = Decimal(self.quantity) * Decimal(self.rate)

    def calculate_amount(self):
        if self.quantity:
            return Decimal(self.quantity) * Decimal(self.rate)
        else:
            # TODO: Handle case for calculation in case of quantity is present
            # since at quantity sqft -> none
            return Decimal(self.sqft) * Decimal(self.rate)

    def discount_amount(self):
        return (self.calculate_amount() * self.discount) / 100

    def total_after_discount(self):
        return self.calculate_amount() - self.discount_amount()

    def get_actual_quantity(self):
        if self.length:
            return self.sqft
        return self.quantity

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.project.pk), str(self.project.name)])


class ProjectTermsAndConditions(models.Model):
    # Project TNC
    heading = models.CharField(max_length=255)
    org_terms = models.ForeignKey(OrganizationTNC, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = RichTextField(null=False)

    def __str__(self):
        return str(self.heading)

    def get_absolute_url(self):
        return reverse(
            "project_terms_and_conditions",
            args=[str(self.project.pk), str(self.project.name)],
        )

    class Meta:
        unique_together = ("project", "org_terms")
        verbose_name = _("Project TNC")
        verbose_name_plural = _("Project TNCs")
