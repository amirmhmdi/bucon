from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, Form, PasswordInput
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


class LaborRegistrationForm(Form):
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)
    email = EmailField()
    phone = CharField(max_length=20)
    password = CharField(widget=PasswordInput)
    repeat_password = CharField(widget=PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            self.add_error("repeat_password", "The passwords do not match.")

        if password:
            user = User(
                username=cleaned_data.get("email", ""),
                first_name=cleaned_data.get("first_name", ""),
                last_name=cleaned_data.get("last_name", ""),
            )
            try:
                password_validation.validate_password(password, user)
            except ValidationError as error:
                self.add_error("password", error)

        return cleaned_data
