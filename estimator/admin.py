from django.contrib import admin

from .models import *


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_on",  "is_deleted"]
    search_fields = [
        "name"
    ]
    search_help_text = "Search by Fields: Name"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "name",
                          "created_on", "is_deleted"]


@admin.register(RoomItem)
class RoomItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_on",  "is_deleted"]
    search_fields = ["name"]
    search_help_text = "Search by Fields: Name"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "name",
                          "created_on", "is_deleted"]


@admin.register(RoomItemDescription)
class RoomItemDescriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "rate", "created_on",  "is_deleted"]
    search_fields = [
        "description"
    ]
    search_help_text = "Search by Fields: Description"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "description", "rate",
                          "created_on", "is_deleted"]


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "project", "room", "room_item",
                    "room_item_description", "quantity", "amount"
                    ]
    search_fields = [
        "project__name",
        "room__name",
        "project__client__name",
        "room_item__name",
        "room_item_description__rate",
    ]

    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id",
                          "project", "room", "room_item",
                          "room_item_description", "quantity", "amount"
                          ]


class ProjectInline(admin.TabularInline):
    model = Estimate
    show_change_link = True
    view_on_site = False
    can_delete = False
    extra = 0
    readonly_fields = [
        "room",
        "room_item",
        "room_item_description",
        "quantity",
        "amount",
    ]
    fields = [
        "room",
        "room_item",
        "room_item_description",
        "quantity",
        "amount",
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "reference_number",
        "created_on",
        "name",
        "client",
    ]
    readonly_fields = [
        "reference_number",
        "deleted_on",
        "created_on",
        "author",
    ]
    inlines = [ProjectInline, ]
