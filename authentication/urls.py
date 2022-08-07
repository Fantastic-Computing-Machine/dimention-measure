from django.urls import path

from authentication.views import OrganizationDetails

urlpatterns = [
    path("myorganization/", OrganizationDetails.as_view(), name="organization"),
]
