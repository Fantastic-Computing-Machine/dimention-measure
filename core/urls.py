from django.urls import path


from .views import DashboardView,SearchView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("search", SearchView.as_view(), name="search"),
]