from django.urls import path

from .views import (
    InspectionHomeView,
    InspectionDetailView,
)

urlpatterns = [
    path("", InspectionHomeView.as_view(), name="inspection_home"),
    path("<int:pk>/<str:inspection_name>/details/", InspectionDetailView.as_view(),
         name="inspection_detail"),
]
