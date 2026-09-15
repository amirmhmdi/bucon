from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ["title", "author", "status", "published_at"]
    list_filter = ["status", "author"]
    search_fields = ["title", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
