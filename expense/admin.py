from django.contrib import admin

from .models import Payee, Expense


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phoneNumber", "total_paid", "total_recieved", "total_pending", "total_noStatus",
                    "description", "updated_on", "created_on"]
    search_fields = [
        "name",
        "phoneNumber",
        "description"
    ]
    search_help_text = "Search by Fields: Name | Username | Description"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "name", "phoneNumber", "total_paid", "total_recieved", "total_pending", "total_noStatus",
                          "description", "updated_on", "created_on"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["id", "payee", "project",
                    "amount", "payment_status", "created_on", "updated_on"]
    search_fields = [
        "payee",
        "project",
        "project__author__first_name",
        "project__author__last_name",
        "project__author__username",
        "payment_status",
        "amount",
    ]
    search_help_text = "Search by Fields: Project | Name | Username | Payment status"
    date_hierarchy = "created_on"
    ordering = ["-created_on"]
    show_full_result_count = True
    list_display_links = ["id", "payee", "project",
                          "amount", "payment_status", "created_on", "updated_on"]
