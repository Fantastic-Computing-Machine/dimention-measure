from django.contrib import admin

from .models import Room, RoomItem, RoomItemDescription, Estimate, Project, ProjectTermsAndConditions
from dimension.admin import soft_delete, soft_undelete


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_on",
        "is_deleted"
    ]
    actions = [soft_delete, soft_undelete]
    readonly_fields = ["deleted_on"]
    search_fields = [
        "name"
    ]
    search_help_text = "Search by Fields: Name"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = [
        "id",
        "name",
        "created_on",
        "is_deleted"
    ]


@admin.register(RoomItem)
class RoomItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_on",
        "is_deleted"
    ]
    search_fields = ["name"]
    search_help_text = "Search by Fields: Name"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    actions = [soft_delete, soft_undelete]
    readonly_fields = ["deleted_on"]
    list_display_links = [
        "id",
        "name",
        "created_on",
        "is_deleted"
    ]


@admin.register(RoomItemDescription)
class RoomItemDescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "description",
        "created_on",
        "is_deleted"
    ]
    search_fields = [
        "description"
    ]
    search_help_text = "Search by Fields: Description"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    readonly_fields = ["deleted_on"]
    show_full_result_count = True
    actions = [soft_delete, soft_undelete]
    list_display_links = [
        "id",
        "description",
        "created_on",
        "is_deleted"
    ]


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "project",
        "room",
        "room_item",
        "room_item_description",
        "quantity",
        "amount"
    ]
    search_fields = [
        "project__name",
        "room__name",
        "project__client__name",
        "room_item__name",
        "room_item_description__rate",
    ]
    actions = [soft_delete, soft_undelete]
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    readonly_fields = ["deleted_on", "created_on",
                       "sqm", "sqft", "amount"]
    list_display_links = [
        "id",
        "project",
        "room",
        "room_item",
        "room_item_description",
        "quantity",
        "amount"
    ]
    list_filter = [
        "created_on",
        "is_deleted",
        "project",
        "room",
        "room_item",
        "room_item_description",
    ]
    fieldsets = (
        ('Project Details', {
            'fields': ('project', 'room', 'room_item', 'room_item_description')
        }),
        ('Measurements', {
            'fields': ('quantity', 'length', 'width', 'sqm', 'sqft', 'unit')
        }),
        ('Financial Details', {
            'fields': ('amount', 'discount', 'rate',)
        }),
        ('Additional Information', {
            'fields': ('created_on', 'is_deleted', 'deleted_on'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('project', 'room', 'room_item', 'room_item_description', 'quantity', 'length', 'width', 'sqm', 'sqft', 'amount', 'discount', 'rate', 'unit'),
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "reference_number",
        "created_on",
        "name",
        "client",
        "is_deleted",
    ]
    readonly_fields = [
        "reference_number",
        "deleted_on",
        "created_on",
        "author",
    ]
    # inlines = [ProjectInline, ]
    list_display_links = [
        "reference_number",
        "created_on",
        "name",
        "client",
    ]
    show_full_result_count = True
    actions = [soft_delete, soft_undelete]
    search_fields = [
        "name",
        "description",
        "client__name",
        "client__phoneNumber"
    ]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'author', 'client', 'created_on')
        }),
        ('Advanced Details', {
            'fields': ('is_deleted', 'deleted_on', 'discount', 'reference_number')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description', 'author', 'client', 'discount', 'reference_number'),
        }),
    )


admin.site.register(ProjectTermsAndConditions)
