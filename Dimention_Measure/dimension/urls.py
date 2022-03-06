from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import HomeView, ProjectView, UpdateDimensionView
from .views import DeleteDimentionView, DeleteProjectView
from .views import download_excel_view


urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # project_id, project_name
    path("project/<int:pk>/<str:project>/",
         ProjectView.as_view(), name="project_detail"),

    # project_id, project_name
    path("project/<int:pk>/<str:project_name>/delete/project/",
         DeleteProjectView, name="delete_project"),

    # dimention_id, project_name
    path("project/<int:pk>/<str:project_name>/update/dimention/",
         UpdateDimensionView.as_view(), name="update_dimention"),

    # dimention_id, project_name
    path("project/<int:pk>/<int:project_id>/<str:project_name>/delete/dimention/",
         DeleteDimentionView, name="delete_dimention"),

    # project_id, project_name
    path("excel/<int:project_id>/<str:project_name>/download/",
         download_excel_view, name="download_excel_file"),
]
