from django.contrib import admin

from .models import Unit, TermsContent, TermsHeading

admin.site.register(Unit)
admin.site.register(TermsHeading)
admin.site.register(TermsContent)
