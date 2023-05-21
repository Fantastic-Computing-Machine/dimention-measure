from django.urls import reverse
from django.contrib.auth import get_user_model as user_model

from django.shortcuts import HttpResponseRedirect
from settings.models import OrganizationTNC
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy


from settings.forms import TermsAndConditionForm
from core.views import BaseAuthClass

User = user_model()


class TermsAndConditions(BaseAuthClass, CreateView):
    model = OrganizationTNC
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

        heading = OrganizationTNC.objects.filter(organization=curr_org)
        context['headings'] = heading
        return context


class ProjectTNC(BaseAuthClass, CreateView):
    model = OrganizationTNC
    form_class = TermsAndConditionForm
    template_name = "project_tnc.html"
    succes_url = reverse_lazy("terms_and_conditions")


def deleteSelectedTnC(request):
    # delete selected terms and conditions
    if request.method == "POST":
        list_to_delete = request.POST.getlist('termsAndConditionCheckBox')
        for item in list_to_delete:
            # WARNING! This is a hard delete, it will delete the item from the database
            OrganizationTNC.objects.filter(id=item).delete()
    return HttpResponseRedirect(reverse('terms_and_conditions'))
