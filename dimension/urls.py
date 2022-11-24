from django.urls import path

from .views import HomeView, ProjectView, UpdateDimensionView
from .views import DeleteDimensionView, DeleteProjectView
from .views import download_excel_view
from .views import MigrateData


urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # project_id, project_name
    path("dimension/project/<int:pk>/<str:project>/details/",
         ProjectView.as_view(), name="project_detail"),

    # project_id, project_name
    path("dimension/project/<int:pk>/<str:project_name>/delete_project/",
         DeleteProjectView, name="delete_project"),

    # dimension_id, project_name
    path("dimension/project/<int:pk>/<str:project_name>/update_dimension/",
         UpdateDimensionView.as_view(), name="update_dimention"),

    # dimension_id, project_id, project_name
    path("dimension/project/<int:pk>/<int:project_id>/<str:project_name>/delete_dimension/",
         DeleteDimensionView, name="delete_dimension"),

    # project_id, project_name
    path("dimension/excel/<int:project_id>/<str:project_name>/download_project/",
         download_excel_view, name="download_excel_file"),

    path("dimension/data/migrate/data/from/mongodb/to/mysqldb/",
         MigrateData.as_view(), name="migrate_view"),
]
