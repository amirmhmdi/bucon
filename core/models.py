from django.db import models


class SiteSettings(models.Model):
    """Singleton row — see save() below. Edited by the admin only."""

    company_name = models.CharField(max_length=100, default="BUCON")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    about_text = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Banner(models.Model):
    """Hero carousel slides on the homepage."""

    title = models.CharField(max_length=150, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="banners/")
    link_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Banner #{self.pk}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
