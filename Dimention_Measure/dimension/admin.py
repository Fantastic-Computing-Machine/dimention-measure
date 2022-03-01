from django.contrib import admin
from .models import Project, Dimension

# qwerty@1234


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "author",
        "total_amount",
        "total_sqm",
        "total_sqft",
        "description",
        "updated_on",
        "created_on"]

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
        "updated_on",
        "total_sqm",
        "total_sqft",
        "total_amount",
    ]


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "project",
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
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "name", "project",
                          "length", "width", "sqm", "sqft", "rate", "amount", "created_on"]
    readonly_fields = [
        "sqm",
        "sqft",
        "amount",
    ]


# @admin.register(Payee)
# class PayeeAdmin(admin.ModelAdmin):
#     list_display = ["id", "name", "phoneNumber",
#                     "description", "updated_on", "created_on"]
#     search_fields = [
#         "name",
#         "phoneNumber",
#         "description"
#     ]
#     search_help_text = "Search by Fields: Name | Username | Description"
#     date_hierarchy = "created_on"
#     ordering = ["-created_on"]
#     show_full_result_count = True
#     list_display_links = ["id", "name", "phoneNumber",
#                           "description", "updated_on", "created_on"]


# @admin.register(Expense)
# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ["id", "payee", "project",
#                     "amount", "payment_status", "created_on", "updated_on"]
#     search_fields = [
#         "payee",
#         "project",
#         "project__author__first_name",
#         "project__author__last_name",
#         "project__author__username",
#         "payment_status",
#         "amount",
#     ]
#     search_help_text = "Search by Fields: Project | Name | Username | Payment status"
#     date_hierarchy = "created_on"
#     ordering = ["-created_on"]
#     show_full_result_count = True
#     list_display_links = ["id", "payee", "project",
#                           "amount", "payment_status", "created_on", "updated_on"]
