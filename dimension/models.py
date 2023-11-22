from django.utils import timezone
from django.contrib.auth import get_user_model as user_model
from django.db import models
from django.urls import reverse

from decimal import Decimal
from typing import List, Dict

from core.templatetags.utility import formatFloat

User = user_model()


def meter2feet(meters):
    # Convert meters to feet
    feet = float(meters) * 3.28084
    inches = round((feet - int(feet)) * 12, 2)
    return feet, inches


class Project(models.Model):
    """
    Represents a project in the system.

    Attributes:
        name (str): Name of the project.
        author (User): User who created the project.
        description (str): Description of the project.
        created_on (datetime): Date and time when the project was created.
        is_deleted (bool): Flag to soft delete the project.
        deleted_on (datetime): Date and time when the project was deleted.
    """

    name = models.CharField(
        max_length=30, unique=False, help_text="Name of the project"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who created the project",
        related_name="dimension_projects",
    )
    description = models.TextField(
        max_length=255, blank=True, null=True, help_text="Description of the project"
    )
    created_on = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the project was created"
    )
    is_deleted = models.BooleanField(
        default=False, help_text="Check to soft delete the project"
    )
    deleted_on = models.DateTimeField(
        blank=True, null=True, help_text="Date and time when the project was deleted"
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        Custom save method to strip and replace spaces in the project name,
        and handle soft deletion by updating the "deleted_on" field.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.name = self.name.strip().replace(" ", "-")
        self.deleted_on = timezone.now() if self.is_deleted else None
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        """
        Calculates the total amount declared in the project.

        Returns:
            Decimal: Total amount declared in the project.
        """
        dims = self.dimensions.filter(project=self, is_deleted=False)
        sum_amount = sum(item.amount for item in dims if item.amount is not None)
        return sum_amount

    @property
    def total_sqm(self):
        """
        Calculates the total square meters declared in the project.

        Returns:
            Decimal: Total square meters declared in the project.
        """
        dims = self.dimensions.filter(project=self, is_deleted=False)
        return sum(item.sqm for item in dims if item.sqm is not None)

    @property
    def total_sqft(self):
        """
        Calculates the total square feet declared in the project.

        Returns:
            Decimal: Total square feet declared in the project.
        """
        dims = self.dimensions.filter(project=self, is_deleted=False)
        return sum(item.sqft for item in dims if item.sqft is not None)

    @property
    def total_running_length(self):
        """
        Calculates the total running length declared in the project.

        Returns:
            Decimal: Total running length declared in the project.
        """
        dims = self.dimensions.filter(
            project=self,
            is_deleted=False,
            width_feet=None or 0.0,
            width_inches=None or 0.0,
        )
        return sum(item.length_feet for item in dims if item.length_feet is not None)


class Dimension(models.Model):
    """
    Represents dimensions associated with a project.

    Attributes:
        project (Project): Project associated with the dimension.
        name (str): Name of the dimension.
        description (str): Description of the dimension.
        length_feet (Decimal): Length in feet.
        length_inches (Decimal): Length in inches.
        width_feet (Decimal): Width in feet.
        width_inches (Decimal): Width in inches.
        sqm (Decimal): Area in square meters.
        sqft (Decimal): Area in square feet.
        rate (Decimal): Rate in rs/sqft.
        amount (Decimal): Calculated amount based on area and rate.
        created_on (datetime): Date and time when the dimension was created.
        is_deleted (bool): Flag to soft delete the dimension.
        deleted_on (datetime): Date and time when the dimension was deleted.
    """

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="dimensions"
    )
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    length_feet = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal("0")
    )
    length_inches = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal("0")
    )

    width_feet = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal("0")
    )
    width_inches = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=Decimal("0")
    )

    sqm = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    sqft = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # rate will be in rs/sqft
    rate = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal("0"))
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.project.name}"

    def save(self, *args, **kwargs):
        """
        Custom save method to handle conversions, calculations, and soft deletion.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
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

        self.rate = Decimal(self.rate)

        self.name = self.name.strip().replace(" ", "-")
        self.description = self.description.strip() if self.description else ""
        self.deleted_on = timezone.now() if self.is_deleted else None

        note = "*Running Length*-"

        # Calculate Area in sqft and sqm
        self.sqft = (length * width) / 144 or None
        self.sqm = self.sqft / Decimal(10.7639) if self.sqft else None

        if self.sqft:
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
        super().save(*args, **kwargs)

    @property
    def length_meter(self) -> str:
        """
        Converts length from feet and inches to meters.

        Returns:
            str: Formatted string representation of the length in meters.
        """
        length_feet = Decimal(self.length_feet) if self.length_feet else Decimal(0)
        length_inches = (
            Decimal(self.length_inches) if self.length_inches else Decimal(0)
        )
        result = ((length_feet * Decimal(12)) + length_inches) * Decimal(0.0254)
        return formatFloat(result)

    @property
    def width_meter(self) -> str:
        """
        Converts width from feet and inches to meters.

        Returns:
            str: Formatted string representation of the width in meters.
        """
        result = Decimal(float(self.width_feet or 0.0) * 0.3048) + Decimal(
            float(self.width_inches or 0) * 0.0254
        )
        return formatFloat(result)

    @classmethod
    def bulk_create_dimensions(cls, dimension_data_list: List[Dict]):
        """Create multiple dimensions object (db-entries) at once"""
        cls.objects.bulk_create([cls(**data) for data in dimension_data_list])

    @classmethod
    def bulk_update_dimensions(cls, dimension_data_list: List[Dict]):
        """Update multiple dimensions at once"""
        instances = [cls(**data) for data in dimension_data_list]
        cls.objects.bulk_update(
            instances,
            [
                "name",
                "description",
                "length_feet",
                "length_inches",
                "width_feet",
                "width_inches",
                "sqm",
                "sqft",
                "rate",
                "amount",
                "created_on",
                "is_deleted",
                "deleted_on",
            ],
        )

    def get_absolute_url(self):
        return reverse(
            "project_detail", args=[str(self.project.pk), str(self.project.name)]
        )
