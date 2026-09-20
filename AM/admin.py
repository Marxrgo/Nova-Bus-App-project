from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LateReport, Announcement

@admin.register(LateReport)
class LateReportAdmin(admin.ModelAdmin):
    list_display = ("slot", "minutes_late", "created_at", "resolved_at", "is_active")
    list_filter = ("slot__loop",)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("loop", "message", "created_at", "resolved_at", "is_active")
