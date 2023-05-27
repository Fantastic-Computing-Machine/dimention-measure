from django.urls import path

from .views import DimensionHomeView, DimensionProjectView, UpdateDimensionView
from .views import DeleteDimensionView, DeleteProjectView
from .views import download_excel_view
# from .views import MigrateData


urlpatterns = [
    path("", DimensionHomeView.as_view(), name="home"),

    # project_id, project_name
    path("project/<int:pk>/<str:project>/details/",
         DimensionProjectView.as_view(), name="project_detail"),

    # project_id, project_name
    path("project/<int:pk>/<str:project_name>/delete_project/",
         DeleteProjectView, name="delete_project"),

    # dimension_id, project_name
    path("project/<int:pk>/<str:project_name>/update_dimension/",
         UpdateDimensionView.as_view(), name="update_dimention"),

    # dimension_id, project_id, project_name
    path("project/<int:pk>/<int:project_id>/<str:project_name>/delete_dimension/",
         DeleteDimensionView, name="delete_dimension"),

    # project_id, project_name
    path("excel/<int:project_id>/<str:project_name>/download_project/",
         download_excel_view, name="download_excel_file"),

]
