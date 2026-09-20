from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import ForcePasswordChangeForm, ProfileUpdateForm
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
		user = User.objects.create_user(username="worker", password="old-password")
		form = ForcePasswordChangeForm(
			user=user,
			data={"new_password1": "short", "new_password2": "short"},
		)

		self.assertFalse(form.is_valid())


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class AccountViewTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="worker", password="old-password")
		self.user.profile.must_change_password = True
		self.user.profile.save()

	def test_force_password_change_updates_password_and_profile(self):
		self.client.force_login(self.user)

		response = self.client.post(
			reverse("accounts:force_password_change"),
			{"new_password1": "new-password-123", "new_password2": "new-password-123"},
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

# Create your tests here.
