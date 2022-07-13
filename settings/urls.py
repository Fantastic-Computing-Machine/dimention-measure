
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from authentication.views import OrganizationDetails

from settings.views import add_terms_heading

urlpatterns = [
    path("add_terms_heading/", add_terms_heading, name="add_terms_heading"),
]
