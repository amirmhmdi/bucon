from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        LABOR = "labor", "Labor"
        MANAGER = "manager", "Manager"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.LABOR)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active_employee = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.role})"

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_labor(self):
        return self.role == self.Role.LABOR
