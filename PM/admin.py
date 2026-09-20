from django.contrib import admin
from .models import BusSlot

# Register your models here.

@admin.register(BusSlot)
class BusSlotAdmin(admin.ModelAdmin):
    list_display = ('loop', 'slot_number', 'bus_number', 'last_updated')
    list_filter = ('loop',)
    search_fields = ('slot_number', 'bus_number')
    ordering = ('loop', 'slot_number')

