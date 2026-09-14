from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # "role" is only meant to be changed here by an admin/superuser —
    # promoting a user to Manager happens by editing this field.
    list_display = ["user", "role", "is_active_employee", "hourly_rate", "must_change_password"]
    list_filter = ["role", "is_active_employee"]
    search_fields = ["user__username", "user__email", "user__first_name", "user__last_name"]
    autocomplete_fields = ["user"]
