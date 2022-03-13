from django.contrib import admin

from .models import Room, RoomItem, RoomItemDescription
from .models import Project
from .models import Estimate

admin.site.register(Room)
admin.site.register(RoomItem)
admin.site.register(RoomItemDescription)
admin.site.register(Project)
admin.site.register(Estimate)
