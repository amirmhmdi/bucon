from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import ContactForm
from .models import Banner, ContactMessage, SiteSettings


class CoreModelTests(TestCase):
	def test_site_settings_is_a_singleton(self):
		first = SiteSettings.objects.create(company_name="First")
		second = SiteSettings(company_name="Second")
		second.save()

		self.assertEqual(first.pk, 1)
		self.assertEqual(second.pk, 1)
		self.assertEqual(SiteSettings.objects.count(), 1)
		self.assertEqual(SiteSettings.load().company_name, "Second")

	def test_banner_string_uses_title_or_primary_key(self):
		banner = Banner.objects.create(
			title="Crafted kitchen", image="banners/kitchen.jpg"
		)
		untitled = Banner.objects.create(
			title="", image="banners/untitled.jpg"
		)

		self.assertEqual(str(banner), "Crafted kitchen")
		self.assertEqual(str(untitled), f"Banner #{untitled.pk}")

	def test_contact_message_defaults_to_unread(self):
		message = ContactMessage.objects.create(
			name="Client", email="client@example.com", message="Please call me."
		)

		self.assertFalse(message.is_read)


class ContactFormTests(TestCase):
	def test_valid_contact_form(self):
		form = ContactForm(
			data={
				"name": "Client",
				"email": "client@example.com",
				"phone": "0123456789",
				"message": "I need a fitted wardrobe.",
				"website": "",
			}
		)

		self.assertTrue(form.is_valid())

	def test_honeypot_rejects_filled_website_field(self):
		form = ContactForm(
			data={
				"name": "Bot",
				"email": "bot@example.com",
				"message": "Spam",
				"website": "https://spam.example",
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("website", form.errors)


@override_settings(
	STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CoreViewTests(TestCase):
	def test_home_shows_only_active_banners_and_featured_published_content(self):
		Banner.objects.create(
			title="Visible", image="banners/visible.jpg", is_active=True
		)
		Banner.objects.create(
			title="Hidden", image="banners/hidden.jpg", is_active=False
		)

		response = self.client.get(reverse("core:home"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			list(response.context["banners"].values_list("title", flat=True)),
			["Visible"],
		)

# Create your tests here.
