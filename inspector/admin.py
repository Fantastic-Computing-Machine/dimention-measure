from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Inspection, Defect, Tag


class InspectionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = [
        "id",
        "name",
        "inspector",
        "is_deleted",
        "created_on",
    ]
    search_fields = [
        "inspector__username",
        "inspector__first_name",
        "inspector__last_name",
        "name",
        "description"
    ]
    search_help_text = "Search by Fields: Inspector | name | Description"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = [
        "inspector",
        "created_on",
        "name",
    ]
    readonly_fields = [
        "deleted_on",
        "inspector",
        "created_on"
    ]
    list_filter = [
        "created_on",
        "deleted_on",
        "inspector__first_name",
        "inspector__last_name",
        "inspector__username",
    ]

    def save_model(self, request, obj, form, change):
        obj.inspector = request.user
        super().save_model(request, obj, form, change)


class DefectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = [
        "title",
        "project",
        "status",
        "created_on",
    ]
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    readonly_fields = [
        "created_on",
        "author",
        "deleted_on",
    ]

    list_filter = [
        "created_on",
        "deleted_on",
        "due_date",
        "is_deleted",
        "project__name",
        "status",
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    # date_hierarchy = "created_on"
    # ordering = ["-created_on"]
    show_full_result_count = True



admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Defect, DefectAdmin)
admin.site.register(Tag, TagAdmin)
