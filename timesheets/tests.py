from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile

from .models import TimesheetEntry


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

