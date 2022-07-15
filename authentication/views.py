from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from authentication.models import Organization
from authentication.forms import OrganizationForm
from settings.models import TermsHeading, TermsContent

# from django.views.generic.edit import FormMixin
# from collections import defaultdict
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import HttpResponseRedirect


User = user_model()


class OrganizationDetails(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_details.html'
    success_url = reverse_lazy("organization")

    def get_object(self):
        queryset = super().get_queryset()
        return queryset.get(pk=self.request.user.organization.pk)

    def get_context_data(self, **kwargs):
        curr_org = self.request.user.organization
        context = super().get_context_data(**kwargs)
        heading = TermsHeading.objects.filter(organization=curr_org)
        content = TermsContent.objects.filter(heading__organization=curr_org)
        context['headings'] = heading

        data = dict()
        for item in heading:
            x = []
            for desc in content:
                if desc.heading == item:
                    x.append(desc)
            data[item] = x

        context['data'] = data

        return context
