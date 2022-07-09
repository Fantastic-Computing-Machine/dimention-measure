from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import (GroupAdmin as BaseGroupAdmin)
from django.contrib.auth.models import (Group as DjangoGroup)
from django.utils.translation import gettext_lazy as _

from authentication.models import Organization, CompanyUser,  Group


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


@admin.register(CompanyUser)
class CompanyUser(admin.ModelAdmin):
    # readonly_fields = ['organization',
    #                    'last_login', 'date_joined', ]

    exclude = ['password', 'is_superuser', 'is_staff']

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     user_access_level = request.user.access_level
    #     is_superuser = request.user.is_superuser

    #     disabled_fields = [
    #         'user_permissions',
    #     ]

    #     if user_access_level == 'SITE_USR':
    #         disabled_fields = disabled_fields + ['is_active']

    #     if user_access_level == 'ORG_ADM':
    #         disabled_fields = disabled_fields + ['organization']

    #     if user_access_level == 'ORG_USR':
    #         disabled_fields |= disabled_fields + \
    #             ['access_level', 'organization', 'is_active']

    #     # Prevent non-superusers from editing their own permissions

    #     for f in disabled_fields:
    #         if f in form.base_fields:
    #             form.base_fields[f].disabled = True

    #     print(form.base_fields['access_level'])

    #     return form


admin.site.register(Organization)


admin.site.unregister(DjangoGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass
