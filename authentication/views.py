from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    UpdateView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model as user_model
from django.views.generic.edit import FormMixin

from authentication.models import Organization
from authentication.forms import OrganizationForm

from settings.models import TermsHeading, TermsContent
from collections import defaultdict

User = user_model()


class OrganizationDetails(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Organization
    context_object_name = 'org'
    form_class = OrganizationForm
    template_name = 'organization/org_details.html'
    success_url = reverse_lazy("home")

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.request.user.organization.pk)

    def get_context_data(self, **kwargs):
        curr_org = self.request.user.organization
        context = super().get_context_data(**kwargs)
        heading = TermsHeading.objects.filter(organization=curr_org)
        content = TermsContent.objects.filter(heading__organization=curr_org)
        context['org'] = curr_org
        context['headings'] = heading
        context['content'] = content

        data = dict()
        for item in heading:
            x = []
            for desc in content:
                if desc.heading == item:
                    x.append(desc)
            data[item] = x

        context['data'] = data

        return context
