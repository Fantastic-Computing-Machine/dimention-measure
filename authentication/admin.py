from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import (GroupAdmin as BaseGroupAdmin)
from django.contrib.auth.models import (Group as DjangoGroup)
from django.utils.translation import gettext_lazy as _

from authentication.models import Organization, CompanyUser,  Group
from authentication.forms import UserChangeForm, UserCreationForm

#new imports
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


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

admin.site.register(Organization)

admin.site.unregister(DjangoGroup)
# admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email','first_name','last_name','organization','phoneNumber','is_admin','is_staff','is_active','last_login')
    list_filter = ('is_admin',)
    fieldsets = (
       ('Authentication', {'fields': ('username', 'password')}),
       ('Personal info', {'fields': ('profile_image','first_name','last_name','gender','date_of_birth','email','phoneNumber','location')}),
       ('Permissions', {'fields': ('organization','is_admin','is_staff','is_active')}),
       ('Activity', {'fields': ('last_login',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
       ('Authentication', {'fields': ('username', 'password1', 'password2')}),
       ('Personal info', {'fields': ('profile_image','first_name','last_name','gender','date_of_birth','email','phoneNumber','location')}),
       ('Permissions', {'fields': ('organization','is_admin','is_staff','is_active')}),
    )
    #readonly
    readonly_fields = ['last_login']
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(CompanyUser, UserAdmin)


# @admin.register(CompanyUser)
# class CompanyUser(admin.ModelAdmin):
#     # readonly_fields = ['organization',
#     #                    'last_login', 'date_joined', ]

#     exclude = ['is_superuser', 'is_staff']

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
