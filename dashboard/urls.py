from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.ManagerDashboardView.as_view(), name="home"),
    # Timesheet approval
    path(
        "timesheets/",
        views.PendingTimesheetListView.as_view(),
        name="pending_timesheets",
    ),
    path(
        "timesheets/all/",
        views.AllTimesheetListView.as_view(),
        name="all_timesheets",
    ),
    path(
        "timesheets/<int:pk>/approve/",
        views.approve_entry,
        name="approve_entry",
    ),
    path(
        "timesheets/<int:pk>/reject/",
        views.reject_entry,
        name="reject_entry",
    ),

    # Contact messages
    path(
        "messages/",
        views.ContactMessageListView.as_view(),
        name="contact_messages",
    ),
    path(
        "messages/<int:pk>/read/",
        views.mark_message_read,
        name="mark_message_read",
    ),

    # Labor accounts
    path("labor/", views.LaborListView.as_view(), name="labor_list"),
    path("labor/new/", views.LaborCreateView.as_view(), name="labor_create"),
    path(
        "labor/<int:pk>/edit/",
        views.LaborUpdateView.as_view(),
        name="labor_update",
    ),
    path(
        "labor/<int:pk>/reset-password/",
        views.reset_labor_password,
        name="reset_password",
    ),

    # Payroll
    path("payroll/", views.PayrollReportView.as_view(), name="payroll_report"),
    path("payroll/export/", views.payroll_csv_export, name="payroll_csv"),
]
