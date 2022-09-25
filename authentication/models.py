from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import Group as DjangoGroup
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
# Gender and Access levels details
GENDER = [
    ("MA", "Male"),
    ("FE", "Female"),
    ("OT", "Others"),
    ("NS", "Prefer not to say"),
]

ACCESS_LEVEL = [
    ("SITE_USR", "SITE USER"),
    ("ORG_ADM", "ORGANIZATION ADMINISTRATOR"),
    ("ORG_USR", "ORGANIZATION USER"),
]


class MyUserManager(BaseUserManager):
    # just user
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # superusers
    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Organization(models.Model):
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255)
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
        return str(self.company_name)

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


class CompanyUser(AbstractBaseUser):
    phoneNumber = models.CharField(
        blank=True,
        null=True,
        validators=[settings.PHONE_NUMBER_FORMAT],
        max_length=11,
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default="NS",
    )
    location = CountryField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_picture/",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
    )
    access_level = models.CharField(
        max_length=8,
        choices=ACCESS_LEVEL,
        default="SITE_USR",
        null=True,
    )
    email = models.EmailField(
        unique=True, max_length=255, null=True, blank=False)
    first_name = models.CharField(max_length=35, blank=True, null=True)
    last_name = models.CharField(max_length=35, blank=True, null=True)
    username = models.CharField(max_length=70, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
    #     return self.is_admin


class Group(DjangoGroup):
    """Instead of trying to get new user under existing `Aunthentication and Authorization`
    banner, create a proxy group model under our Accounts app label.
    Refer to: https://github.com/tmm/django-username-email/blob/master/cuser/admin.py
    """
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
