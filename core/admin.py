from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Banner, ContactMessage, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(SummernoteModelAdmin):
    summernote_fields = ("about_text",)

    def has_add_permission(self, request):
        # singleton — block adding a second row
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active"]
    list_editable = ["order", "is_active"]
    ordering = ["order"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "is_read", "created_at"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "message"]
    actions = ["mark_as_read"]

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
