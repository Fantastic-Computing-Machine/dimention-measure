from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from .views import *


urlpatterns = [
    # path("", HomeView.as_view(), name="home"),
    # path("project/<int:pk>/<str:project>",
    #      # project_id, project_name
    #      ProjectView.as_view(), name="project_detail"),

    # path("project/<int:pk>/<str:project>/delete/project/",
    #      # project_id, project_name
    #      DeleteProjectView.as_view(), name="delete_project"),

    # path("project/<int:pk>/<str:project_name>/update/dimention/",
    #      # dimention_id, project_name
    #      UpdateDimensionView.as_view(), name="update_dimention"),

    # path("project/<int:pk>/<str:name>/delete/dimention/",
    #      # dimention_id, project_name
    #      DeleteDimentionView.as_view(), name="delete_dimention"),
]
