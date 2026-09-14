from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Every user gets a Profile automatically. Superusers created via
    createsuperuser also get one, defaulting to the labor role — promote
    them to manager from the admin if needed."""
    if created:
        Profile.objects.get_or_create(user=instance)
