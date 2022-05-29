from django.contrib import admin
from django.db import models
from django.forms import Textarea

from client_and_company.models import Client, CompanyDetail


admin.site.register(CompanyDetail)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = [
        "id", "name", "phoneNumber",
        "town_city",  "state", "is_deleted"
    ]
    search_fields = [
        "name",
        "phoneNumber",
        "landmark",
        "zip_code",
        "town_city",
        "state",
    ]
    search_help_text = "Search by Fields: Name, Phone Number, city, state, zip_code"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = [
        "id", "name", "phoneNumber",
        "town_city",  "state", "is_deleted"
    ]
    readonly_fields = ['deleted_on', 'organization']

    list_filter = [
        'created_on',
        'organization__name',
        'state',
    ]

    def save_model(self, request, obj):
        if getattr(obj, "added_by", None) is None:
            obj.organization == request.user.organization
        obj.save()
