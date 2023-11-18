from django.urls import reverse_lazy
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from authentication.models import Organization
from authentication.forms import OrganizationForm
from core.views import BaseAuthClass

User = user_model()


class OrganizationDetails(BaseAuthClass, LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organization/org_details.html"
    success_url = reverse_lazy("organization")

    def get_object(self):
        return self.request.user.organization

    def put(self):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
