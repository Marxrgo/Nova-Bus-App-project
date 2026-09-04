from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from loops.models import BusSlot, Looptype


class TimedStatusBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.expires_at and not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=60)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        if self.resolved_at:
            return False
        if self.expires_at and timezone.now() >= self.expires_at:
            return False
        return True

    def resolve(self):
        self.resolved_at = timezone.now()
        self.save(update_fields=["resolved_at"])


class LateReport(TimedStatusBase):
    slot = models.ForeignKey(BusSlot, on_delete=models.CASCADE, related_name="late_reports")
    minutes_late = models.PositiveIntegerField(help_text="Estimated delay in minutes")
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.slot} — {self.minutes_late} min late"


class Announcement(TimedStatusBase):
    loop = models.CharField(
        max_length=10, choices=Looptype.choices, null=True, blank=True,
        help_text="Leave blank for a system-wide announcement"
    )
    message = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        scope = self.get_loop_display() if self.loop else "All Loops"
        return f"[{scope}] {self.message[:40]}"
