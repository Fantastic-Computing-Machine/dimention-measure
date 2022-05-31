from django_countries.fields import CountryField

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as DjangoGroup
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _


from django.conf import settings

# STATE_CHOICES = (
#     ("Andhra Pradesh", "Andhra Pradesh"),
#     ("Arunachal Pradesh ", "Arunachal Pradesh "),
#     ("Assam", "Assam"),
#     ("Bihar", "Bihar"),
#     ("Chhattisgarh", "Chhattisgarh"),
#     ("Goa", "Goa"),
#     ("Gujarat", "Gujarat"),
#     ("Haryana", "Haryana"),
#     ("Himachal Pradesh", "Himachal Pradesh"),
#     ("Jammu and Kashmir ", "Jammu and Kashmir "),
#     ("Jharkhand", "Jharkhand"),
#     ("Karnataka", "Karnataka"), ("Kerala", "Kerala"),
#     ("Madhya Pradesh", "Madhya Pradesh"),
#     ("Maharashtra", "Maharashtra"),
#     ("Manipur", "Manipur"),
#     ("Meghalaya", "Meghalaya"),
#     ("Mizoram", "Mizoram"),
#     ("Nagaland", "Nagaland"),
#     ("Odisha", "Odisha"),
#     ("Punjab", "Punjab"),
#     ("Rajasthan", "Rajasthan"),
#     ("Sikkim", "Sikkim"),
#     ("Tamil Nadu", "Tamil Nadu"),
#     ("Telangana", "Telangana"),
#     ("Tripura", "Tripura"),
#     ("Uttar Pradesh", "Uttar Pradesh"),
#     ("Uttarakhand", "Uttarakhand"),
#     ("West Bengal", "West Bengal"),
#     ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
#     ("Chandigarh", "Chandigarh"),
#     ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
#     ("Daman and Diu", "Daman and Diu"),
#     ("Lakshadweep", "Lakshadweep"),
#     ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
#     ("Puducherry", "Puducherry")
# )

# from django.contrib.auth import get_user_model as user_model
# User = user_model()

GENDER = [
    ("MA", "Male"),
    ("FE", "Female"),
    ("OT", "Others"),
    ("NS", "Prefer not to say"),
]


class Organization(models.Model):
    company_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phoneNumber = models.CharField(blank=True,
                                   validators=[settings.PHONE_NUMBER_FORMAT], max_length=11)
    address_1 = models.CharField(max_length=255, default="abc")
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    state = models.CharField(choices=settings.STATE_CHOICES,
                             max_length=255, default='abc')

    def __str__(self):
        return str(self.company_name) + ' | ' + str(self.name)

    def save(self):
        self.address_1 = self.address_1.strip()
        if self.address_2:
            self.address_2 = self.address_2.strip()
        if self.landmark:
            self.landmark = self.landmark.strip()
        self.town_city = self.town_city.strip()
        return super(Organization, self).save()

    def address(self):
        full_address = self.address_1
        if self.address_2:
            full_address = full_address + ", " + self.address_2
        if self.landmark:
            full_address = full_address + ", " + self.landmark
        full_address = full_address + ", " + self.town_city + \
            ", " + self.state + " - " + self.zip_code
        return full_address


class CompanyUser(AbstractUser):
    phoneNumber = models.CharField(blank=True,
                                   validators=[settings.PHONE_NUMBER_FORMAT], max_length=11)
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default="NS",
    )
    location = CountryField()

    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_picture/",
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.username)

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()


class Group(DjangoGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
