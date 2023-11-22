from django.urls import path

from .views import (
    CheckProjectNameView,
    DimensionHomeView,
    DimensionProjectView,
    UpdateProjectView,
    UpdateDimensionView,
    DeleteDimensionView,
    DeleteProjectView,
    download_excel_view
)


urlpatterns = [
    path("", DimensionHomeView.as_view(), name="home"),

    # project_id, project_name
    path("project/<int:pk>/<str:project>/details/",
         DimensionProjectView.as_view(), name="project_detail"),

    # project_id, project_name
    path("project/<int:pk>/<str:project_name>/delete_project/",
         DeleteProjectView, name="delete_project"),

    # project_id, project_name
    path("project/<int:pk>/<str:project_name>/update_project/",
         UpdateProjectView.as_view(), name="update_project"),

    # dimension_id, project_name
    path("project/<int:pk>/<str:project_name>/update_dimension/",
         UpdateDimensionView.as_view(), name="update_dimention"),

    # dimension_id, project_id, project_name
    path("project/<int:pk>/<int:project_id>/<str:project_name>/delete_dimension/",
         DeleteDimensionView, name="delete_dimension"),

    # project_id, project_name
    path("excel/<int:project_id>/<str:project_name>/download_project/",
         download_excel_view, name="download_excel_file"),
    
    path('check_project_name/', CheckProjectNameView.as_view(), name='check_project_name'),

]
