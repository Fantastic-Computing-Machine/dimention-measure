from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import HomeView, ProjectView, UpdateDimensionView
from .views import DeleteDimentionView
from .views import DeleteProjectView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # project_id, project_name
    path("project/<int:pk>/<str:project>/",
         ProjectView.as_view(), name="project_detail"),

    path("project/<int:pk>/<str:project_name>/delete/project/",
         # project_id, project_name
         DeleteProjectView, name="delete_project"),

    # dimention_id, project_name
    path("project/<int:pk>/<str:project_name>/update/dimention/",
         UpdateDimensionView.as_view(), name="update_dimention"),

    path("project/<int:pk>/<int:project_id>/<str:project_name>/delete/dimention/",
         # dimention_id, project_name
         DeleteDimentionView, name="delete_dimention"),
]
