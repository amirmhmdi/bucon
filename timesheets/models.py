from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class TimesheetEntry(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    labor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="timesheet_entries"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.PositiveIntegerField(default=0)
    total_hours = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False, default=0
    )
    description = models.TextField(help_text="What did you work on today?")

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_entries",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("labor", "date", "start_time")
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.labor} — {self.date} ({self.status})"

    def _compute_total_hours(self):
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        if end <= start:
            # entry spans past midnight
            end += timedelta(days=1)
        worked = (end - start) - timedelta(minutes=self.break_minutes)
        hours = max(worked.total_seconds(), 0) / 3600
        return round(hours, 2)

    def save(self, *args, **kwargs):
        self.total_hours = self._compute_total_hours()
        super().save(*args, **kwargs)

    @property
    def is_editable(self):
        return self.status != self.Status.APPROVED
