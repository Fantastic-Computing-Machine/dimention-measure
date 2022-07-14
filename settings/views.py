from django.urls import reverse
from django.contrib.auth import get_user_model as user_model

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from settings.models import TermsHeading, TermsContent

User = user_model()


@login_required
def add_terms_heading(request):
    print(request.POST)
    if request.method == 'POST':
        TermsHeading.objects.create(
            name=str(request.POST['name']),
            organization=request.user.organization
        )
        return HttpResponseRedirect(reverse('organization'))


@login_required
def add_terms_content(request):
    print(request.POST)
    if request.method == 'POST':
        TermsContent.objects.create(
            heading=TermsHeading.objects.filter(
                pk=int(request.POST['condition_heading']))[0],
            description=request.POST['description'],
        )
        return HttpResponseRedirect(reverse('organization'))
