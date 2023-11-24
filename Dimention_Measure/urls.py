"""Dimention_Measure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include

from core.views import HealthCheckView

urlpatterns = [
    path("dimension/", include("dimension.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/console/", admin.site.urls),
    path("settings/", include("settings.urls")),
    path("user/", include("django.contrib.auth.urls")),
    path("user/", include("authentication.urls")),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.EXPENSE_ENABLED:
    urlpatterns.append(path("expense/", include("expense.urls")))

if settings.ESTIMATE_ENABLED:
    estimate_views = [
        path("estimate/", include("estimator.urls")),
        path("client-and-company/", include("client_and_company.urls")),
    ]
    urlpatterns += estimate_views

health_views = [
    path("health/", include("health_check.urls")),
    path("health/ping/", HealthCheckView.as_view(), name="health"),
    path("health/data/", include("watchman.urls")),
]

urlpatterns += health_views
