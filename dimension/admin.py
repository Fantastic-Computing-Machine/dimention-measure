from django.contrib import admin
from .models import Project, Dimension

from django.db import models
from django.forms import Textarea


class ProjectInline(admin.TabularInline):
    model = Dimension
    show_change_link = True
    view_on_site = False
    can_delete = False
    extra = 0
    readonly_fields = ['name', "length",
                       "width", "sqm", "sqft", "rate", "amount", "deleted_on", "description"]
    fields = ['name', "length",
              "width", "sqm", "sqft", "rate", "amount", "description"]


class ProjectTabular(admin.StackedInline):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    model = Dimension
    show_change_link = True
    view_on_site = False
    can_delete = False
    extra = 1
    readonly_fields = [
        "sqm",
        "sqft",
        "amount",
        "deleted_on",
    ]
    exclude = ["is_deleted"]

    def get_queryset(self, request):
        return Dimension.objects.none()


# @admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    inlines = [ProjectInline, ProjectTabular]
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

    # def get_queryset(self, request):
    #     qs = super(ProjectAdmin, self).get_queryset(request)
    #     return qs.filter(author__organization=request.user.organization)

    def save_model(self, request, obj, form, change):
        self.author = request.user
        # if getattr(obj, "added_by", None) is None:
        #     obj.author == request.user
        # obj.save()


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
