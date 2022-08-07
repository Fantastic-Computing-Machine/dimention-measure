from django.urls import path

from client_and_company.views import UpdateClientView, ClientView, DeleteClient


urlpatterns = [
    path("clients/", ClientView.as_view(), name="clients"),

    path("clients/update/<int:pk>/<str:client_name>/",
         UpdateClientView.as_view(), name="update_client"),

    path("clients/<int:pk>/delete/", DeleteClient, name="delete_client"),
]
