from django.urls import path

from . import views

app_name = "timesheets"

urlpatterns = [
    path("", views.TimesheetEntryListView.as_view(), name="list"),
    path("new/", views.TimesheetEntryCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.TimesheetEntryUpdateView.as_view(), name="update"),
]
