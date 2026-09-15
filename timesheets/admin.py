from django.contrib import admin

from .models import TimesheetEntry


@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ["labor", "date", "start_time", "end_time", "total_hours", "status"]
    list_filter = ["status", "date"]
    search_fields = ["labor__username", "labor__email", "description"]
    readonly_fields = ["total_hours"]
