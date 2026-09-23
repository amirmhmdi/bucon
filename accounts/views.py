from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ForcePasswordChangeForm, ProfileUpdateForm


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
