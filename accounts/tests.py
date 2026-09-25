from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import (
    ForcePasswordChangeForm,
    LaborRegistrationForm,
    ProfileUpdateForm,
)
from .models import Profile


class ProfileSignalTests(TestCase):
    def test_new_user_gets_a_labor_profile(self):
        user = User.objects.create_user(username="worker", password="password")

        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertTrue(user.profile.is_labor)


class AccountFormTests(TestCase):
    def test_profile_form_does_not_expose_privileged_fields(self):
        self.assertEqual(set(ProfileUpdateForm().fields), {"phone", "photo"})

    def test_force_password_form_rejects_short_password(self):
        user = User.objects.create_user(
            username="worker", password="old-password"
        )
        form = ForcePasswordChangeForm(
            user=user,
            data={"new_password1": "short", "new_password2": "short"},
        )

        self.assertFalse(form.is_valid())


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class AccountViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="worker", password="old-password"
        )
        self.user.profile.must_change_password = True
        self.user.profile.save()

    def test_force_password_change_updates_password_and_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:force_password_change"),
            {
                "new_password1": "new-password-123",
                "new_password2": "new-password-123",
            },
        )

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("core:post_login_redirect"))
        self.assertTrue(self.user.check_password("new-password-123"))
        self.assertFalse(self.user.profile.must_change_password)

    def test_profile_page_redirects_anonymous_users(self):
        response = self.client.get(reverse("accounts:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class LaborRegistrationTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            "first_name": "New",
            "last_name": "Worker",
            "email": "new.worker@example.com",
            "phone": "0123456789",
            "password": "Strong-password-123!",
            "repeat_password": "Strong-password-123!",
        }
        data.update(overrides)
        return data

    def test_registration_requires_all_labor_fields(self):
        form = LaborRegistrationForm()

        self.assertTrue(all(field.required for field in form.fields.values()))

    def test_labor_can_register_and_is_logged_in(self):
        response = self.client.post(
            reverse("accounts:register"), self.valid_data()
        )

        user = User.objects.get(email="new.worker@example.com")
        self.assertRedirects(
            response, reverse("timesheets:list"), fetch_redirect_response=False
        )
        self.assertEqual(user.profile.role, Profile.Role.LABOR)
        self.assertEqual(user.profile.phone, "0123456789")
        self.assertFalse(user.profile.must_change_password)
        self.assertTrue(user.check_password("Strong-password-123!"))
        self.assertEqual(int(response.wsgi_request.user.pk), user.pk)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="password",
        )

        response = self.client.post(
            reverse("accounts:register"),
            self.valid_data(email="EXISTING@example.com"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")
        self.assertEqual(
            User.objects.filter(email__iexact="existing@example.com").count(),
            1,
        )

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:register"),
            self.valid_data(repeat_password="Different-password-123!"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "passwords do not match")
