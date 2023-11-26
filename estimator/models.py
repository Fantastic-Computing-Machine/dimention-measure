from ckeditor.fields import RichTextField
from datetime import datetime
from django.utils import timezone
from typing import List, Dict, Tuple
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

    def save(self, *args, **kwargs):
        self.name = self.name.replace(" ", "-").strip()
        if self.is_deleted:
            self.deleted_on = datetime.now()
        if not self.is_deleted:
            self.deleted_on = None
        key = not self.pk
        super().save(*args, **kwargs)
        if key:
            self.reference_number = str(datetime.now().year) + "/" + str(self.pk)
            kwargs["force_insert"] = False
            super().save(*args, **kwargs)
        return

    @property
    def total_amount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_amount = sum(item.total_after_discount() for item in estimates)
        return sum_amount

    @property
    def total_itemized_discount(self):
        estimates = Estimate.objects.filter(project=self, is_deleted=False)
        sum_discount = sum(item.discount_amount() for item in estimates)
        return sum_discount

    @property
    def discount_amount(self):
        return (self.total_amount * self.discount) / 100

    @property
    def total_after_discount(self):
        return self.total_amount - self.discount_amount

    @property
    def gst_amount(self):
        return Decimal(format(self.total_after_discount * Decimal(0.18), ".2f"))

    @property
    def total_with_gst(self):
        return self.total_after_discount + self.gst_amount

    def get_all_rooms(self):
        estimate_room_obj = (
            Estimate.objects.values_list("room__id", "room__name")
            .filter(project__id=self.pk)
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
        max_digits=20, decimal_places=5, blank=True, null=True, default=Decimal(0)
    )
    length = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True, default=Decimal(0)
    )
    width = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True, default=Decimal(0)
    )
    sqm = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True, default=Decimal(0)
    )
    sqft = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True, default=Decimal(0)
    )
    amount = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=False, default=Decimal(0)
    )
    discount = models.DecimalField(
        max_digits=20, decimal_places=5, validators=zero2hundred, default=Decimal(0)
    )
    rate = models.DecimalField(max_digits=20, decimal_places=5, default=Decimal(0))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.project.name) + " | " + str(self.room.name)

    def save(self, *args, **kwargs):
        """Business Logic: Save and compute for the estimate"""

        if self.is_deleted:
            self.deleted_on = timezone.now()
            super().save(*args, **kwargs)
        else:
            self.deleted_on = None

        self.length = Decimal(self.length) if self.length else Decimal(0)
        self.width = Decimal(self.width) if self.width else Decimal(0)
        self.quantity = Decimal(self.quantity) if self.quantity else Decimal(0)
        self.rate = Decimal(self.rate) if self.rate else Decimal(0)
        self.discount = Decimal(self.discount) if self.discount else Decimal(0)

        if self.width and self.length and not self.quantity:
            # compute for area
            self.sqm, self.sqft, self.amount = self.compute_for_area(
                self.width, self.length, self.rate
            )
        elif self.quantity and not self.width and not self.length:
            # compute for quantity
            self.sqm, self.sqft, self.amount = self.compute_for_quantity(
                self.quantity, self.rate
            )
        else:
            # compute for running feet
            self.sqm, self.sqft, self.amount = self.compute_for_rft(
                self.length, self.rate
            )

        super().save(*args, **kwargs)

    def compute_for_area(
        self, width: Decimal, length: Decimal, rate: Decimal
    ) -> Tuple[Decimal, Decimal, Decimal]:
        """Set area of the estimate"""
        sqm = Decimal(length) * Decimal(width)
        sqft = sqm * Decimal(10.7639)
        amount = sqft * Decimal(rate)
        return sqm, sqft, amount

    def compute_for_quantity(
        self, quantity: Decimal, rate: Decimal
    ) -> Tuple[Decimal, Decimal, Decimal]:
        """Compute for Quantity"""
        sqm = Decimal(0)
        sqft = Decimal(0)
        amount = Decimal(quantity) * Decimal(rate)
        return sqm, sqft, amount

    def compute_for_rft(
        self, length: Decimal, rate: Decimal
    ) -> Tuple[Decimal, Decimal, Decimal]:
        """Compute for Running Feet"""
        sqm = length
        sqft = sqm * Decimal(3.28084)
        amount = sqft * Decimal(rate)
        return sqm, sqft, amount

    def discount_amount(self):
        return (self.amount * self.discount) / 100

    def total_after_discount(self):
        return self.amount - self.discount_amount()

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
