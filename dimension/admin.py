from django.contrib import admin
from .models import Project, Dimension

from django.db import models
from django.forms import Textarea


class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = [
        "id",
        "name",
        "author",
        "total_amount",
        "total_sqm",
        "total_sqft",
        "description",
        "created_on",
    ]
    search_fields = [
        "author__username",
        "author__first_name",
        "author__last_name",
        "name",
        "description"
    ]
    search_help_text = "Search by Fields: Author | name | Description"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = [
        "author",
        "description",
        "created_on",
        "name",
        "total_sqm",
        "total_sqft",
        "total_amount",
    ]
    readonly_fields = ["deleted_on", "author"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = ["name", "project",
                    "length", "width", "sqm", "sqft", "rate", "amount", "created_on"]
    search_fields = [
        "name",
        "project",
        "project__author__first_name",
        "project__author__last_name",
        "project__author__username",
        "description"
    ]
    search_help_text = "Search by Fields: Project | Name | Username | Description"
    date_hierarchy = "created_on"
    ordering = ["-project", "-is_deleted", "-created_on"]
    show_full_result_count = True
    list_display_links = ["name", "project",
                          "length", "width", "sqm", "sqft", "rate", "amount", "created_on"]

    fields = ["name", "project", "description",
              "length", "width", "sqm", "sqft", "rate", "amount", "created_on"]
    readonly_fields = ["sqm", "sqft", "amount", "deleted_on", "created_on"]
    list_filter = [
        "created_on",
        "is_deleted",
        "deleted_on",
        "project"
    ]

    def get_queryset(self, request):
        qs = super(DimensionAdmin, self).get_queryset(request)
        return qs.filter(project__author__organization=request.user.organization)


admin.site.register(Project, ProjectAdmin)
