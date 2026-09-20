from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import Profile

from .models import TimesheetEntry
from .forms import TimesheetEntryForm


class TimesheetEntryDeleteTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="labor", password="test-password")
		self.user.profile.role = Profile.Role.LABOR
		self.user.profile.must_change_password = False
		self.user.profile.save()
		self.client.login(username="labor", password="test-password")

	def create_entry(self, status):
		return TimesheetEntry.objects.create(
			labor=self.user,
			date=date(2026, 9, 16),
			start_time=time(9),
			end_time=time(17),
			status=status,
			description="Site work",
		)

	def test_labor_can_delete_pending_entry(self):
		entry = self.create_entry(TimesheetEntry.Status.PENDING)

		response = self.client.post(
			reverse("timesheets:update", args=[entry.pk]),
			{"action": "delete"},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("timesheets:list"))
		self.assertFalse(TimesheetEntry.objects.filter(pk=entry.pk).exists())

	def test_labor_can_delete_rejected_entry(self):
		entry = self.create_entry(TimesheetEntry.Status.REJECTED)

		response = self.client.post(
			reverse("timesheets:update", args=[entry.pk]),
			{"action": "delete"},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("timesheets:list"))
		self.assertFalse(TimesheetEntry.objects.filter(pk=entry.pk).exists())

	def test_labor_cannot_delete_approved_entry(self):
		entry = self.create_entry(TimesheetEntry.Status.APPROVED)

		response = self.client.post(
			reverse("timesheets:update", args=[entry.pk]),
			{"action": "delete"},
		)

		self.assertEqual(response.status_code, 403)
		self.assertTrue(TimesheetEntry.objects.filter(pk=entry.pk).exists())


class TimesheetModelAndFormTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="worker", password="password")

	def test_total_hours_supports_overnight_work(self):
		entry = TimesheetEntry.objects.create(
			labor=self.user,
			date=date(2026, 9, 20),
			start_time=time(22),
			end_time=time(2),
			break_minutes=30,
			description="Night work",
		)

		self.assertEqual(entry.total_hours, 3.5)

	def test_equal_start_and_end_times_are_rejected(self):
		form = TimesheetEntryForm(
			data={
				"date": "2026-09-20",
				"start_time": "09:00",
				"end_time": "09:00",
				"break_minutes": 0,
				"description": "Invalid shift",
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("End time must be different", str(form.errors))

@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class TimesheetAccessTests(TestCase):
	def setUp(self):
		self.labor = User.objects.create_user(username="worker", password="password")
		self.labor.profile.role = Profile.Role.LABOR
		self.labor.profile.must_change_password = False
		self.labor.profile.save()
		self.other_labor = User.objects.create_user(username="other", password="password")
		self.other_labor.profile.role = Profile.Role.LABOR
		self.other_labor.profile.must_change_password = False
		self.other_labor.profile.save()
		self.entry = TimesheetEntry.objects.create(
			labor=self.other_labor,
			date=date(2026, 9, 20),
			start_time=time(9),
			end_time=time(17),
			description="Private work",
		)

	def test_labor_list_contains_only_the_current_users_entries(self):
		self.client.force_login(self.labor)

		response = self.client.get(reverse("timesheets:list"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["entries"].count(), 0)

	def test_labor_cannot_edit_another_users_entry(self):
		self.client.force_login(self.labor)

		response = self.client.get(reverse("timesheets:update", args=[self.entry.pk]))

		self.assertEqual(response.status_code, 404)

