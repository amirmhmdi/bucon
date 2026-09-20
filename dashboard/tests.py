from datetime import date, time
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import Profile
from dashboard.views import PayrollReportView
from timesheets.models import TimesheetEntry


class AllTimesheetListViewTests(TestCase):
	def setUp(self):
		self.manager = User.objects.create_user(username="manager", password="test-password")
		self.manager.profile.role = Profile.Role.MANAGER
		self.manager.profile.must_change_password = False
		self.manager.profile.save()

		self.labor = User.objects.create_user(
			username="labor@example.com",
			email="labor@example.com",
			first_name="Site",
			last_name="Worker",
			password="test-password",
		)
		self.labor.profile.role = Profile.Role.LABOR
		self.labor.profile.hourly_rate = 25
		self.labor.profile.must_change_password = False
		self.labor.profile.save()
		self.client.login(username="manager", password="test-password")

	def create_entry(self, description, entry_date, start_hour=9):
		return TimesheetEntry.objects.create(
			labor=self.labor,
			date=entry_date,
			start_time=time(start_hour),
			end_time=time(17),
			break_minutes=60,
			description=description,
		)

	@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
	def test_manager_can_filter_timesheets_and_newest_same_day_entry_is_first(self):
		older = self.create_entry("Older work", date(2026, 9, 16), start_hour=9)
		newer = self.create_entry("Newer work", date(2026, 9, 16), start_hour=10)
		self.create_entry("Different day", date(2026, 9, 15))

		response = self.client.get(
			reverse("dashboard:all_timesheets"),
			{"labor": self.labor.pk, "start_date": "2026-09-16", "end_date": "2026-09-16"},
		)

		entries = list(response.context["entries"])
		self.assertEqual(response.status_code, 200)
		self.assertEqual(entries, [newer, older])
		self.assertEqual(entries[0].daily_wage, 150)

	def test_non_manager_cannot_access_all_timesheets(self):
		self.client.force_login(self.labor)

		response = self.client.get(reverse("dashboard:all_timesheets"))

		self.assertEqual(response.status_code, 403)


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class ManagerWorkflowTests(TestCase):
	def setUp(self):
		self.manager = User.objects.create_user(username="manager", password="password")
		self.manager.profile.role = Profile.Role.MANAGER
		self.manager.profile.must_change_password = False
		self.manager.profile.save()
		self.labor = User.objects.create_user(username="worker", password="password")
		self.labor.profile.role = Profile.Role.LABOR
		self.labor.profile.must_change_password = False
		self.labor.profile.hourly_rate = 20
		self.labor.profile.save()
		self.entry = TimesheetEntry.objects.create(
			labor=self.labor,
			date=date(2026, 9, 20),
			start_time=time(8),
			end_time=time(16),
			break_minutes=30,
			description="Roof framing",
		)
		self.client.force_login(self.manager)

	def test_manager_dashboard_counts_pending_entries(self):
		response = self.client.get(reverse("dashboard:home"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["pending_timesheets"], 1)
		self.assertEqual(response.context["all_timesheets_count"], 1)

	def test_pending_list_excludes_approved_entries(self):
		self.entry.status = TimesheetEntry.Status.APPROVED
		self.entry.save()

		response = self.client.get(reverse("dashboard:pending_timesheets"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["entries"].count(), 0)

	def test_manager_can_approve_entry(self):
		response = self.client.post(reverse("dashboard:approve_entry", args=[self.entry.pk]))

		self.entry.refresh_from_db()
		self.assertRedirects(response, reverse("dashboard:pending_timesheets"))
		self.assertEqual(self.entry.status, TimesheetEntry.Status.APPROVED)
		self.assertEqual(self.entry.approved_by, self.manager)
		self.assertIsNotNone(self.entry.approved_at)

	def test_manager_can_reject_entry_with_reason(self):
		response = self.client.post(
			reverse("dashboard:reject_entry", args=[self.entry.pk]),
			{"rejection_reason": "Please add the site address."},
		)

		self.entry.refresh_from_db()
		self.assertRedirects(response, reverse("dashboard:pending_timesheets"))
		self.assertEqual(self.entry.status, TimesheetEntry.Status.REJECTED)
		self.assertEqual(self.entry.rejection_reason, "Please add the site address.")

	def test_labor_cannot_approve_entry(self):
		self.client.force_login(self.labor)

		response = self.client.post(reverse("dashboard:approve_entry", args=[self.entry.pk]))

		self.assertEqual(response.status_code, 403)
		self.entry.refresh_from_db()
		self.assertEqual(self.entry.status, TimesheetEntry.Status.PENDING)

	def test_payroll_rows_use_approved_hours_and_rate(self):
		self.entry.status = TimesheetEntry.Status.APPROVED
		self.entry.save()

		view = PayrollReportView()
		rows = view._build_rows(date(2026, 9, 20), date(2026, 9, 20))

		self.assertEqual(len(rows), 1)
		self.assertEqual(rows[0]["total_hours"], Decimal("7.50"))
		self.assertEqual(rows[0]["total_pay"], Decimal("150.00"))

	def test_payroll_ignores_pending_entries(self):
		view = PayrollReportView()

		self.assertEqual(view._build_rows(date(2026, 9, 20), date(2026, 9, 20)), [])

# Create your tests here.
