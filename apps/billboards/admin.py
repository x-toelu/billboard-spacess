from django.contrib import admin

from .models import Billboard


class BillboardAdmin(admin.ModelAdmin):
    list_filter = ('is_verified', 'size', 'is_booked')
    list_display = ('owner', 'full_location', 'price',
                    'is_verified', 'is_booked')
    search_fields = ('state',)


admin.site.register(Billboard, BillboardAdmin)
