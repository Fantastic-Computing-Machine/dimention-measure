from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Project, Dimension, Collection


@admin.action(description="Soft-delete")
def soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=True)


@admin.action(description="Soft-undelete")
def soft_undelete(modeladmin, request, queryset):
    queryset.update(is_deleted=False)


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    fields = [
        "name",
        "author",
        "description",
        "created_on",
        "total_sqm",
        "total_sqft",
        "total_amount",
    ]
    readonly_fields = [
        "name",
        "author",
        "description",
        "created_on",
        "total_sqm",
        "total_sqft",
        "total_amount",
    ]
    can_delete = False
    view_on_site = False
    show_change_link = True
    ordering = ["-created_on"]
    verbose_name_plural = "Projects"
    verbose_name = "Project"
    show_full_result_count = True
    max_num = 0


class CollectionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    inlines = [ProjectInline]
    list_display = [
        "name",
        "author",
        "description",
        "created_on",
        "is_deleted",
    ]
    search_fields = [
        "author__username",
        "author__first_name",
        "author__last_name",
        "name",
        "description",
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
    ]
    readonly_fields = [
        "deleted_on",
        "author",
        "created_on",
    ]
    actions = [soft_delete, soft_undelete]
    list_filter = [
        "created_on",
        "is_deleted",
        "deleted_on",
    ]
    fieldsets = (
        ("Information", {"fields": ("name", "author", "created_on")}),
        ("Project Details", {"fields": ("description", "is_deleted", "deleted_on")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "author", "description"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class DimensionInline(admin.TabularInline):
    model = Dimension
    extra = 0
    fields = [
        "name",
        "author",
        "sqm",
        "sqft",
        "amount",
        "created_on",
    ]
    readonly_fields = [
        "name",
        "author",
        "created_on",
        "sqm",
        "sqft",
        "amount",
    ]
    can_delete = False
    show_change_link = True
    view_on_site = False
    ordering = ["-created_on"]
    verbose_name_plural = "Dimensions"
    verbose_name = "Dimension"
    max_num = 0


class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    inlines = [DimensionInline]
    list_display = [
        "name",
        "author",
        "collection",
        "total_amount",
        "total_sqm",
        "total_running_length",
        "description",
        "created_on",
        "is_deleted",
    ]
    search_fields = [
        "author__username",
        "author__first_name",
        "author__last_name",
        "name",
        "collection__name",
        "description",
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
        "total_amount",
    ]
    readonly_fields = [
        "deleted_on",
        "author",
        "created_on",
        "total_sqm",
        "total_amount",
        "total_running_length",
        "total_sqft",
    ]
    actions = [soft_delete, soft_undelete]
    list_filter = [
        "author",
        "is_deleted",
        "collection",
        "created_on",
    ]
    fieldsets = (
        ("Information", {"fields": (("name", "collection"), ("author", "created_on"))}),
        ("Project Details", {"fields": ("description", ("is_deleted", "deleted_on"))}),
        (
            "Statistics",
            {
                "fields": (
                    ("total_sqm", "total_sqft"),
                    "total_amount",
                    "total_running_length",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "author", "description"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    actions = [soft_delete, soft_undelete]
    list_display = ["name", "project", "author", "created_on", "is_deleted"]
    search_fields = [
        "name",
        "project",
        "project__author__first_name",
        "project__author__last_name",
        "project__author__username",
        "description",
    ]
    search_help_text = "Search by Fields: Project | Name | Username | Description"
    date_hierarchy = "created_on"
    ordering = ["-project", "-is_deleted", "-created_on"]
    show_full_result_count = True
    list_display_links = ["name", "project", "author", "created_on", "is_deleted"]
    readonly_fields = ["sqm", "sqft", "amount", "deleted_on", "created_on"]
    list_filter = [
        "author",
        "project__author",
        "project__collection",
        "created_on",
        "is_deleted",
        "deleted_on",
        "project",
    ]
    fieldsets = (
        (None, {"fields": ("project", "name", "author", "created_on")}),
        (
            "Dimension Details",
            {
                "fields": (
                    "description",
                    ("length_feet", "length_inches"),
                    ("width_feet", "width_inches"),
                    ("sqm", "sqft"),
                    ("rate", "amount"),
                )
            },
        ),
        (
            "Deletion Details",
            {
                "fields": ("is_deleted", "deleted_on"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("project", "name", "description", "rate"),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super(DimensionAdmin, self).get_queryset(request)
        return qs.filter(project__author__organization=request.user.organization)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Collection, CollectionAdmin)
