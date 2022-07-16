from django.urls import reverse
from django.contrib.auth import get_user_model as user_model

from django.shortcuts import HttpResponseRedirect
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
    template_name = "tnc.html"
    succes_url = reverse_lazy("terms_and_conditions")

    # def post(self, request):
    #     print(request.POST)

    #     # request.POST._mutable = True
    #     # request.POST["organization"] = str(request.user.organization.id)
    #     # request.POST._mutable = False

    #     # TermsHeading(name=request.POST['name'])
    #     form = TermsAndConditionForm(request.POST)
    #     try:
    #         if form.is_valid():
    #             # form.save()
    #             obj = form.save(commit=False)
    #             obj.organization = request.user.organization

    #             print(obj)
    #             obj.save()
    #     except:
    #         print(form.error())
    #     return super(TermsAndConditions, self).post(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_org = self.request.user.organization
        heading = TermsHeading.objects.filter(organization=curr_org)
        context['headings'] = heading
        return context
