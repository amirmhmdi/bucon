from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class LaborCreateForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    temporary_password = forms.CharField(widget=forms.PasswordInput)
    hourly_rate = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["temporary_password"],
        )
        # accounts.signals auto-creates the Profile; fill in the rest here.
        profile = user.profile
        profile.role = Profile.Role.LABOR
        profile.hourly_rate = data["hourly_rate"]
        profile.must_change_password = True
        profile.save()
        return user


class LaborUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["hourly_rate", "phone", "is_active_employee"]


class ResetPasswordForm(forms.Form):
    temporary_password = forms.CharField(widget=forms.PasswordInput)


class PayrollFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class TimesheetFilterForm(forms.Form):
    labor = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role=Profile.Role.LABOR).order_by("first_name", "last_name", "email"),
        required=False,
        empty_label="All users",
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    sort = forms.ChoiceField(
        choices=(
            ("newest", "Newest dates first"),
            ("oldest", "Oldest dates first"),
        ),
        required=False,
        initial="newest",
    )
