from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    readonly_fields = [
        "name", "description", "image", "start_date",
        "end_date", "start_time", "end_time", "location",
    ]


admin.site.register(Event, EventAdmin)
