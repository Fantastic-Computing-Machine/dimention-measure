from django.contrib import admin
from django.db import models
from django.forms import Textarea

from client_and_company.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = [
        "id",
        "name",
        "phoneNumber",
        "town_city",
        "state",
        "is_deleted",
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
        "id",
        "name",
        "phoneNumber",
        "town_city",
        "state",
        "is_deleted",
    ]
    readonly_fields = [
        'deleted_on',
        'organization',
        'created_by',
    ]
    list_filter = [
        'created_on',
        'organization__company_name',
        'state',
    ]

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
