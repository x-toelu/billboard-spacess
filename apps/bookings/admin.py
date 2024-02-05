from django.contrib import admin

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)
    list_display = ['user', 'billboard', 'timeline', 'period', 'is_paid']
    list_filter = ['is_paid', 'period']


admin.site.register(Booking, BookingAdmin)
