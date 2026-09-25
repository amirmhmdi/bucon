from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import (
    ForcePasswordChangeForm,
    LaborRegistrationForm,
    ProfileUpdateForm,
)
from .models import Profile


@login_required
def force_password_change(request):
    if request.method == "POST":
        form = ForcePasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            profile = request.user.profile
            profile.must_change_password = False
            profile.save(update_fields=["must_change_password"])
            messages.success(request, "Password updated.")
            return redirect("core:post_login_redirect")
    else:
        form = ForcePasswordChangeForm(user=request.user)

    return render(
        request, "accounts/force_password_change.html", {"form": form}
    )


@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": profile},
    )


def labor_register(request):
    if request.method == "POST":
        form = LaborRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data["email"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=data["password"],
            )
            profile = user.profile
            profile.phone = data["phone"]
            profile.role = Profile.Role.LABOR
            profile.must_change_password = False
            profile.save()
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            messages.success(request, "Your labor account has been created.")
            return redirect("timesheets:list")
    else:
        form = LaborRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
