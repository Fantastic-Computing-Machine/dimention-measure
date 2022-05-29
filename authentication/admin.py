from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib import admin

from authentication.models import UserProfile


admin.site.register(UserProfile)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    readonly_fields = [
        "object_id",
        "object_repr",
        "change_message",
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

# admin.site.unregister(User)

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     readonly_fields = [
#         'date_joined',
#         'last_login',
#     ]

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser
#         disabled_fields = set()

#         if not is_superuser:
#             disabled_fields |= {
#                 'username',
#                 'is_superuser',
#                 'user_permissions',
#             }

#         # Prevent non-superusers from editing their own permissions
#         print(obj)
#         if (
#             not is_superuser
#             and obj is not None
#             and obj == request.user
#         ):
#             disabled_fields |= {
#                 'is_staff',
#                 'is_superuser',
#                 'groups',
#                 'user_permissions',
#             }

#         for f in disabled_fields:
#             if f in form.base_fields:
#                 form.base_fields[f].disabled = True

#         return form

#     def clean(self):
#         print("hello")
#         return
