from django.contrib import admin
from .models import Bus, BusStatus

# Register your models here.


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    search_fields = ("number",)

@admin.register(BusStatus)
class BusStatusAdmin(admin.ModelAdmin):
    list_display = ("bus", "date", "is_late", "arrived_time", "updated_at")
    list_filter = ("date", "is_late")