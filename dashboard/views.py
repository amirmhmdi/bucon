from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView

from timesheets.models import TimesheetEntry


class ManagerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_manager:
            return HttpResponseForbidden("Manager access only.")
        return super().dispatch(request, *args, **kwargs)


class PendingTimesheetListView(ManagerRequiredMixin, ListView):
    model = TimesheetEntry
    template_name = "dashboard/pending_timesheets.html"
    context_object_name = "entries"

    def get_queryset(self):
        return TimesheetEntry.objects.filter(status=TimesheetEntry.Status.PENDING)


def approve_entry(request, pk):
    if not request.user.profile.is_manager:
        return HttpResponseForbidden()
    entry = get_object_or_404(TimesheetEntry, pk=pk)
    entry.status = TimesheetEntry.Status.APPROVED
    entry.approved_by = request.user
    entry.approved_at = timezone.now()
    entry.save()
    messages.success(request, f"Approved {entry.labor}'s entry for {entry.date}.")
    return redirect("dashboard:pending_timesheets")


def reject_entry(request, pk):
    if not request.user.profile.is_manager:
        return HttpResponseForbidden()
    entry = get_object_or_404(TimesheetEntry, pk=pk)
    if request.method == "POST":
        entry.status = TimesheetEntry.Status.REJECTED
        entry.rejection_reason = request.POST.get("rejection_reason", "")
        entry.approved_by = request.user
        entry.approved_at = timezone.now()
        entry.save()
        messages.success(request, f"Rejected {entry.labor}'s entry for {entry.date}.")
        return redirect("dashboard:pending_timesheets")
    return render(request, "dashboard/reject_entry.html", {"entry": entry})

