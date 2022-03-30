from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import *


urlpatterns = [
    path("", AllEstimates.as_view(), name="all_estimates"),
    path("<int:pk>/<str:project_name>/details",
         EstimateDetailView.as_view(), name="estimate"),
]
