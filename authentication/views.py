from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponseRedirect,render,redirect
from audioop import reverse
import http
from http.client import HTTPResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView

from authentication.models import Organization
from authentication.forms import OrganizationForm
from settings.models import TermsHeading, TermsContent
from django.views.generic.edit import FormMixin, ProcessFormView


User = user_model()


class OrganizationDetails(LoginRequiredMixin, UpdateView):
    login_url = '/user/login/'
    redirect_field_name = 'redirect_to'
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_details.html'
    success_url = reverse_lazy("organization")

    def get_object(self):
        return self.request.user.organization

    # def post(self, request):
    #     print(request.POST)
    #     form = OrganizationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         print("Valid and Saved")
    #     else:
    #         print(form.errors)
    #     return super(OrganizationDetails, self).post(request)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,request, form):
        print("Hello")
        print(form.cleaned_data)
        org = self.get_object()
        org.company_name = request.POST['company_name']
        org.manager_name = request.POST['manager_name']
        org.email = request.POST['email']
        org.phoneNumber = request.POST['phoneNumber']
        org.address1 = request.POST.get('address1', "")
        org.address2 = request.POST.get('address2', "")
        org.landmark = request.POST['landmark']
        org.town_city = request.POST['town_city']
        org.zip_code = request.POST['zip_code']
        org.state = request.POST['state']
        org.save()
        return render(request, 'organization/org_details.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_org = self.request.user.organization
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


# @login_required
# def update_organization_details(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = OrganizationForm(request.POST)
#         if form.is_valid():
#             print(form.save())
#             print("Form Valid and Saved")
#         else:
#             print(form.errors)
#         print("Organization details submitted")
#     return HttpResponseRedirect(reverse('organization'))


#  action="{% url 'organization_update' %}"
