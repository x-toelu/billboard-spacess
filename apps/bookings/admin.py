from django.contrib import admin

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)
    list_display = ['user', 'billboard', 'timeline', 'period', 'paid']
    list_filter = ['paid', 'period']


admin.site.register(Booking, BookingAdmin)
