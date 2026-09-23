from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "password/change/",
        views.force_password_change,
        name="force_password_change",
    ),
    path("profile/", views.profile_update, name="profile"),
]
