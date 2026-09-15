from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.ManagerDashboardView.as_view(), name="home"),
    # Timesheet approval
    path("timesheets/", views.PendingTimesheetListView.as_view(), name="pending_timesheets"),
    path("timesheets/<int:pk>/approve/", views.approve_entry, name="approve_entry"),
    path("timesheets/<int:pk>/reject/", views.reject_entry, name="reject_entry"),

    # Contact messages
    path("messages/", views.ContactMessageListView.as_view(), name="contact_messages"),
    path("messages/<int:pk>/read/", views.mark_message_read, name="mark_message_read"),
]
