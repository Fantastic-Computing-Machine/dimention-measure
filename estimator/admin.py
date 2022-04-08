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
    search_fields = [
        "name"
    ]
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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
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


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ["id",
                    "project", "room", "room_item",
                    "room_item_description",  "unit", "quantity", "amount"
                    ]
    search_fields = [
        "project__name",
        "room__name",
        "project__client__name",
        "room_item__name",
        "room_item_description__rate",
    ]

    # x = ["id",
    #      "project__name", "project__client__name", "room__name", "room_item__name",
    #      "room_item_description__rate",  "unit__unit", "quantity", "amount"
    #      ]
    # search_help_text = "Search by Fields: Name, Phone Number, city, state, zip_code"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id",
                          "project", "room", "room_item",
                          "room_item_description",  "unit", "quantity", "amount"
                          ]


admin.site.register(Project)
admin.site.register(Unit)
