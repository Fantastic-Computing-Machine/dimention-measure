from django.conf import settings
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
import django.db

from rest_framework.views import APIView
from rest_framework.response import Response

from dimension.models import Project as DimensionProject

if settings.ESTIMATE_ENABLED:
    from estimator.models import Project as EstimateProject


User = user_model()


class BaseAuthClass(LoginRequiredMixin):
    """Class to be inherited by all views that require login"""

    login_url = "/user/login/"
    redirect_field_name = "next_to"


class DashboardView(BaseAuthClass, TemplateView):
    """
    Class view for dashboard page
    """

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        # get data fro dimension section
        kwargs["dimensions"] = DimensionProject.objects.filter(
            is_deleted=False,
            author__organization=self.request.user.organization,
        ).order_by("-created_on")[:5]

        # get data from estimate section if enabled

        kwargs["estimates"] = (
            EstimateProject.objects.filter(
                is_deleted=False,
                client__is_deleted=False,
                author__organization=self.request.user.organization,
            ).order_by("-created_on")[:5]
            if settings.ESTIMATE_ENABLED
            else []
        )

        return super().get_context_data(**kwargs)


# TODO: Search for Project name and Tags within the project.
# For this create a new page and render results on that with toggles b/w
# 1. Dimension and Estimate
# 2. Project and Tags


class SearchView(BaseAuthClass, APIView):
    """
    Class view for search page
    """

    def post(self, request, format=None):
        if request.data.get("type") == "dimension":
            dimensions = DimensionProject.objects.filter(
                is_deleted=False, name__icontains=request.data["textToSearch"]
            )
            results = []
            for dimension in dimensions:
                results_item = dict()
                results_item["title"] = dimension.name.capitalize()
                results_item["url"] = reverse(
                    "project_detail", args=[str(dimension.pk), str(dimension.name)]
                )
                results_item["created_on"] = dimension.created_on.date()

                results.append(results_item)

            return Response({"success": True, "results": results})
        elif settings.ESTIMATE_ENABLED and request.data.get("type") == "estimate":
            estimates = EstimateProject.objects.filter(
                is_deleted=False, name__icontains=request.data["textToSearch"]
            )
            results = []
            for estimate in estimates:
                results_item = dict()
                results_item["title"] = estimate.name.capitalize()
                results_item["url"] = reverse(
                    "estimate", args=[str(estimate.pk), str(estimate.name)]
                )
                results_item["created_on"] = estimate.created_on.date()

                results.append(results_item)
            return Response({"success": True, "results": results})
        return Response({"success": False, "results": []})


class HealthCheckView(APIView):
    def get(self, request, format=None):
        if not django.db.connection.ensure_connection():
            return Response({"success": True}, status=200)
        return Response({"success": False}, status=500)


class LoggedInUsersView(APIView):
    """
    Class view for getting logged in users
    """

    template_name = "logged_in_users.html"

    def get_context_data(self, **kwargs):
        active_users = get_active_logged_in_users()
        kwargs["active_users"] = active_users

        # return super().get_context_data(**kwargs)
