from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

from authentication.views import OrganizationDetails

urlpatterns = [
    path("myorganization/", OrganizationDetails.as_view(), name="organization"),
    # path("myorganization/update/", update_organization_details,
    #      name="organization_update"),
]
