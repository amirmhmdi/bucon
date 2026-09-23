from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from portfolio.models import Project
from blog.models import Post

from .forms import ContactForm
from .models import Banner


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks — your message has been sent.")
            return redirect("core:home")
    else:
        form = ContactForm()

    context = {
        "banners": Banner.objects.filter(is_active=True),
        "featured_projects": Project.objects.filter(
            status=Project.Status.PUBLISHED, is_featured=True
        )[:6],
        "featured_posts": Post.objects.filter(
            status=Post.Status.PUBLISHED, is_featured=True
        )[:3],
        "contact_form": form,
    }
    return render(request, "core/home.html", context)


@login_required
def post_login_redirect(request):
    """Sends a freshly logged-in user to the right place based on role."""
    profile = request.user.profile

    if profile.must_change_password:
        return redirect("accounts:force_password_change")

    if profile.is_manager:
        return redirect("dashboard:home")

    return redirect("timesheets:list")
