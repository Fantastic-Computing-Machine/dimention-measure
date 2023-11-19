# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
from django.db import models
from django.urls import reverse

from decimal import Decimal
from datetime import datetime

from core.templatetags.utility import formatFloat

User = user_model()


def meter2feet(meters):
    # Convert meters to feet
    feet = float(meters) * 3.28084
    inches = round((feet - int(feet)) * 12, 2)
    return feet, inches


class Project(models.Model):
    name = models.CharField(
        max_length=30, unique=False, help_text="Name of the project"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who created the project"
    )
    description = models.TextField(
        max_length=255, blank=True, null=True, help_text="Description of the project"
    )
    created_on = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the project was created"
    )
    is_deleted = models.BooleanField(
        default=False, help_text="Check to soft Delete the project"
    )
    deleted_on = models.DateTimeField(
        blank=True, null=True, help_text="Date and time when the project was deleted"
    )

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
        sum_amount = sum(item.amount for item in dims if item.amount is not None)
        return sum_amount

    def total_sqm(self):
        # to calculate total sqm declared in project
        dims = Dimension.objects.filter(project=self, is_deleted=False)
        sum_sqm = sum(item.sqm for item in dims if item.sqm is not None)
        return sum_sqm

    def total_sqft(self):
        # to calculate total sqft declared in project
        dims = Dimension.objects.filter(project=self, is_deleted=False)
        sum_sqft = sum(item.sqft for item in dims if item.sqft is not None)
        return sum_sqft

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.pk), str(self.name)])


class Dimension(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    length_feet = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    length_inches = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )

    width_feet = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    width_inches = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal("0")
    )

    sqm = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # rate will be in rs/sqft
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.project.name}"

    def save(self):
        self.length_feet = Decimal(self.length_feet) if self.length_feet else Decimal(0)
        self.length_inches = (
            Decimal(self.length_inches) if self.length_inches else Decimal(0)
        )
        self.width_feet = Decimal(self.width_feet) if self.width_feet else Decimal(0)
        self.width_inches = (
            Decimal(self.width_inches) if self.width_inches else Decimal(0)
        )

        # convert feet to inches for easy calculation
        length = (self.length_feet * 12) + self.length_inches
        width = (self.width_feet * 12) + self.width_inches

        self.rate = Decimal(self.rate) if self.rate else Decimal(0)

        self.name = self.name.strip().replace(" ", "-")
        self.description = self.description.strip() if self.description else ""
        self.deleted_on = datetime.now() if self.is_deleted else None

        note = "*Running Length*-"

        # Calculate Area in sqft and sqm
        self.sqft = (length * width) / 144 or None
        self.sqm = self.sqft / Decimal(10.7639) if self.sqft else None

        if self.rate and self.sqft:
            # Area
            self.amount = self.rate * self.sqft
            if self.description:
                self.description = self.description.replace(note, "")
        elif not width:
            # Running Length
            self.amount = (self.rate * length) / 12

            self.description = (
                f"{note}{self.description}"
                if note not in self.description
                else self.description
            )
        else:
            # No Rate
            self.amount = Decimal(0)

        return super(Dimension, self).save()

    def length_meter(self):
        result = Decimal(float(self.length_feet) * 0.3048) + Decimal(
            float(self.length_inches) * 0.0254
        )
        return formatFloat(result)

    def width_meter(self):
        result = Decimal(float(self.width_feet or 0.0) * 0.3048) + Decimal(
            float(self.width_inches or 0) * 0.0254
        )
        return formatFloat(result)

    def get_absolute_url(self):
        return reverse(
            "project_detail", args=[str(self.project.pk), str(self.project.name)]
        )
