from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.ManagerDashboardView.as_view(), name="home"),
    path("timesheets/", views.PendingTimesheetListView.as_view(), name="pending_timesheets"),
    path("timesheets/<int:pk>/approve/", views.approve_entry, name="approve_entry"),
    path("timesheets/<int:pk>/reject/", views.reject_entry, name="reject_entry"),
]
