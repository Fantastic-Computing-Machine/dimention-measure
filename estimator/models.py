from django_countries.fields import CountryField
import decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models


STATE_CHOICES = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"), ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),
    ("Lakshadweep", "Lakshadweep"),
    ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
    ("Puducherry", "Puducherry")
)


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
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.description) + " @ " + str(self.rate)


class Client(models.Model):
    name = models.CharField(
        max_length=255)
    description = models.TextField(
        max_length=255, blank=True, null=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(blank=True,
                                   validators=[phoneNumberRegex], max_length=11)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    address_1 = models.CharField(max_length=255, default="abc")
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    state = models.CharField(choices=STATE_CHOICES,
                             max_length=255, default='abc')

    def __str__(self):
        return str(self.name) + ' | ' + str(self.phoneNumber)

    def save(self):
        self.name = self.name.replace(" ", "-").strip()
        if self.description:
            self.description = self.description.strip()
        self.address_1 = self.address_1.strip()
        if self.address_2:
            self.address_2 = self.address_2.strip()
        if self.landmark:
            self.landmark = self.landmark.strip()
        self.town_city = self.town_city.strip()
        return super(Client, self).save()

    def get_absolute_url(self):
        return reverse("clients")


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
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
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
        sum_amount = sum(item.calculate_amount() for item in estimates)
        return sum_amount

    def gst_amount(self):
        return decimal.Decimal(format(self.total_amount() * decimal.Decimal(0.18), ".2f"))

    def total_with_gst(self):
        return self.total_amount() + self.gst_amount()

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.pk), str(self.name)])


class Unit(models.Model):
    unit = models.CharField(max_length=255)

    def __str__(self):
        return str(self.unit)


class Estimate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_item = models.ForeignKey(RoomItem, on_delete=models.CASCADE)
    room_item_description = models.ForeignKey(
        RoomItemDescription, on_delete=models.CASCADE)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, blank=True, null=True, default=1)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.project.name) + ' | ' + str(self.room.name)

    def save(self):
        self.amount = decimal.Decimal(
            self.quantity) * self.room_item_description.rate
        return super(Estimate, self).save()

    def calculate_amount(self):
        return decimal.Decimal(self.quantity) * self.room_item_description.rate

    def get_absolute_url(self):
        return reverse("estimate", args=[str(self.project.pk), str(self.project.name)])
