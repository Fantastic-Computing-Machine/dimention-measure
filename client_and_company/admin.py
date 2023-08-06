from django.contrib import admin
from django.db import models
from django.forms import Textarea

from client_and_company.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    list_display = [
        "id",
        "name",
        "phoneNumber",
        "organization",
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
        "organization",
        "state",
        "is_deleted",
    ]
    readonly_fields = [
        "deleted_on",
        "organization",
        "created_by",
        "created_on",
    ]
    list_filter = [
        "created_on",
        "organization__company_name",
        "state",
        "is_deleted",
    ]

    fieldsets = (
        (
            "General Information",
            {
                "fields": ("name", "description", "tax_id"),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phoneNumber",
                    "address_1",
                    "address_2",
                    "landmark",
                    "town_city",
                    "zip_code",
                    "state",
                ),
            },
        ),
        (
            "Project Information",
            {
                "fields": (
                    "project_address_1",
                    "project_address_2",
                    "project_landmark",
                    "project_town_city",
                    "project_zip_code",
                    "project_state",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Other Details",
            {
                "fields": (
                    "organization",
                    "created_by",
                    "created_on",
                    "is_deleted",
                    "deleted_on",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.organization = request.user.organization
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
