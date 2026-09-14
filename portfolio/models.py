from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/")
    client_name = models.CharField(max_length=100, blank=True)
    completed_on = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title}"
