from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

import decimal
from django_countries.fields import CountryField
from datetime import datetime

# from django.contrib.auth import get_user_model as user_model
# User = user_model()

GENDER = [
    ("MA", "Male"),
    ("FE", "Female"),
    ("OT", "Others"),
    ("NS", "Prefer not to say"),
]

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")


class CompanyUser(AbstractUser):
    phoneNumber = models.CharField(blank=True,
                                   validators=[phoneNumberRegex], max_length=11)
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

    def __str__(self):
        return str(self.username)

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()
