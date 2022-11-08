from django.contrib import admin

from .models import Unit, OrganizationTNC

admin.site.register(Unit)


@admin.register(OrganizationTNC)
class OrganizationTNCAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_display_links = ('name', 'organization')
    list_filter = ['organization']
