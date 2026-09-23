from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)
    list_display = [
        "title",
        "status",
        "is_featured",
        "completed_on",
        "created_by",
    ]
    list_filter = ["status", "is_featured"]
    search_fields = ["title", "client_name"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
