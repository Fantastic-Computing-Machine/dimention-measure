from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import gettext_lazy as _

from authentication.models import Organization, CompanyUser, Group
from authentication.forms import UserChangeForm, UserCreationForm
from .utils import get_active_logged_in_users

User = user_model()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drill-down navigation in the admin page
    date_hierarchy = "action_time"
    # to filter the results by users, content types and action flags
    list_filter = ["user", "content_type", "action_flag"]
    # when searching the user will be able to search in both object_repr and change_message
    search_fields = ["object_repr", "change_message"]
    list_display = [
        "action_time",
        "user",
        "content_type",
        "action_flag",
    ]
    readonly_fields = [
        "object_id",
        "object_repr",
        "change_message",
        "action_time",
        "user",
        "content_type",
        "action_flag",
    ]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "organization",
        "phoneNumber",
        "is_admin",
        "is_staff",
        "is_active",
        "last_login",
    )
    list_filter = ("is_admin", "is_staff", "is_active", "organization", "last_login")
    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "profile_image",
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "email",
                    "phoneNumber",
                    "location",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "organization",
                    "is_admin",
                    "is_staff",
                    "is_active",
                    "access_level",
                )
            },
        ),
        ("Activity", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        ("Authentication", {"fields": ("username", "password1", "password2")}),
        (
            "Personal info",
            {
                "fields": (
                    "profile_image",
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "email",
                    "phoneNumber",
                    "location",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("organization", "is_admin", "is_staff", "is_active")},
        ),
    )
    readonly_fields = ["last_login"]
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("company_name", "manager_name", "email", "registered_on")

    list_filter = ("state", "registered_on")
    readonly_fields = ["registered_on", "deleted_on"]
    search_fields = ("company_name", "manager_name", "email", "town_city")
    ordering = ("-registered_on",)
    fieldsets = (
        (
            "General Information",
            {"fields": ("company_name", "manager_name", "email", "website", "gstn")},
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
                )
            },
        ),
        (
            "Bank Details",
            {
                "fields": (
                    "bank_account_holder_name",
                    "bank_account_number",
                    "bank_name",
                    "bank_branch",
                    "bank_ifsc_code",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Other Details",
            {
                "fields": ("registered_on", "is_active", "is_deleted", "deleted_on"),
                "classes": ("collapse",),
            },
        ),
    )


class LoggedInUsersAdmin(admin.ModelAdmin):
    def current_logged_in_users(self, obj=None):
        active_users = get_active_logged_in_users()
        return ", ".join([user.username for user in active_users])

    current_logged_in_users.short_description = "Current Logged In Users"

    list_display = (
        "current_logged_in_users",
        "username",
        "last_login",
    )
    list_display_links = None
    actions = None
    list_filter = (
        "organization",
        "last_login",
    )


class LoggedInUser(User):
    class Meta:
        proxy = True


admin.site.register(LoggedInUser, LoggedInUsersAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CompanyUser, UserAdmin)
admin.site.unregister(DjangoGroup)
# admin.site.unregister(Group)
