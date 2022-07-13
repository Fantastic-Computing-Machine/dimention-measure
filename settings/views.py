from django.urls import reverse
from django.contrib.auth import get_user_model as user_model

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect

from settings.forms import TermsHeadingForm

User = user_model()


@login_required
def add_terms_heading(request):
    print(request.POST)
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST["organization_id"] = request.user.organization.id
        request.POST._mutable = False

        print('----------------------------------------')
        print(request.POST)
        print('----------------------------------------')
        form = TermsHeadingForm(request.POST)

        if form.is_valid():
            form.save()
        print('----------------------------------------')
        return HttpResponseRedirect(reverse('organization'))
