from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class ForcePasswordChangeMiddleware:
    """If the logged-in user's profile has must_change_password=True,
    redirect every request to the "set new password" page until they
    change it — except for a short exempt list (that page itself, logout,
    static/media, summernote's editor assets)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated and not user.is_staff:
            profile = getattr(user, "profile", None)
            if profile and profile.must_change_password:
                current_url_name = resolve(request.path_info).view_name
                if current_url_name not in settings.FORCE_PASSWORD_CHANGE_EXEMPT_URL_NAMES:
                    return redirect("accounts:force_password_change")

        return self.get_response(request)
