from django.contrib import admin

from .models import *

admin.site.register(Room)
admin.site.register(RoomItem)
admin.site.register(RoomItemDescription)
admin.site.register(Project)
admin.site.register(Estimate)
admin.site.register(Client)
