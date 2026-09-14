from django.contrib.auth.forms import SetPasswordForm
from django.forms import ModelForm

from .models import Profile


class ForcePasswordChangeForm(SetPasswordForm):
    """Reuses Django's built-in SetPasswordForm (no old password required —
    the user is already authenticated via the temporary password)."""


class ProfileUpdateForm(ModelForm):
    """Fields a labor is allowed to edit on their own profile.
    Deliberately excludes role and hourly_rate."""

    class Meta:
        model = Profile
        fields = ["phone", "photo"]
