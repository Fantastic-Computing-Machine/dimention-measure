from django.urls import reverse
from django.contrib.auth import get_user_model as user_model

from django.shortcuts import HttpResponseRedirect
from authentication.models import Organization
from settings.models import TermsHeading
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy


from settings.forms import TermsAndConditionForm

User = user_model()


class TermsAndConditions(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = TermsHeading
    form_class = TermsAndConditionForm
    template_name = "org_tnc.html"
    succes_url = reverse_lazy("terms_and_conditions")

    def post(self, request):

        request.POST._mutable = True
        request.POST["organization"] = str(request.user.organization.id)
        request.POST._mutable = False

        form = TermsAndConditionForm(request.POST)
        try:
            if form.is_valid():
                form.save()
        except:
            print(form.error())

        return HttpResponseRedirect(reverse('terms_and_conditions'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_org = self.request.user.organization
        heading = TermsHeading.objects.filter(organization=curr_org)
        context['headings'] = heading
        return context


class ProjectTNC(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = TermsHeading
    form_class = TermsAndConditionForm
    template_name = "project_tnc.html"
    succes_url = reverse_lazy("terms_and_conditions")
