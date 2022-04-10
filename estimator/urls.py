from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import *


urlpatterns = [
    path("", AllEstimates.as_view(), name="all_estimates"),

    path("<int:pk>/<str:project_name>/details/",
         EstimateDetailView.as_view(), name="estimate"),

    path("<int:pk>/<str:project_name>/update_estimate/",
         UpdateEstimateProjectView.as_view(), name="update_estimate_project"),

    path("folio/", FolioView.as_view(), name="folio"),

    path("clients/", ClientView.as_view(), name="clients"),

    path("clients/update/<int:pk>/<str:client_name>/",
         UpdateClientView.as_view(), name="update_client"),
         
    path("estimate/<int:pk>/<str:project_name>/delete",DeleteEstimate, name="delete_estimate"),
]
