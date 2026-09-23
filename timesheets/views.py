from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import TimesheetEntryForm
from .models import TimesheetEntry


class LaborRequiredMixin(LoginRequiredMixin):
    """Restricts a view to users with role=labor."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_labor:
            return HttpResponseForbidden("Labor access only.")
        return super().dispatch(request, *args, **kwargs)


class TimesheetEntryListView(LaborRequiredMixin, ListView):
    model = TimesheetEntry
    template_name = "timesheets/entry_list.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        return TimesheetEntry.objects.filter(labor=self.request.user)


class TimesheetEntryCreateView(LaborRequiredMixin, CreateView):
    model = TimesheetEntry
    form_class = TimesheetEntryForm
    template_name = "timesheets/entry_form.html"
    success_url = reverse_lazy("timesheets:list")

    def form_valid(self, form):
        form.instance.labor = self.request.user
        messages.success(self.request, "Timesheet entry submitted.")
        return super().form_valid(form)


class TimesheetEntryUpdateView(LaborRequiredMixin, UpdateView):
    model = TimesheetEntry
    form_class = TimesheetEntryForm
    template_name = "timesheets/entry_form.html"
    success_url = reverse_lazy("timesheets:list")

    def get_queryset(self):
        return TimesheetEntry.objects.filter(labor=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        entry = getattr(self, "object", None)
        if entry and not entry.is_editable:
            return HttpResponseForbidden(
                "This entry has been approved and can no longer be edited."
            )
        return response

    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "delete":
            entry = self.get_object()
            if not entry.is_editable:
                return HttpResponseForbidden(
                    "This entry has been approved and can no longer be "
                    "deleted."
                )
            entry.delete()
            messages.success(request, "Timesheet entry deleted.")
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.instance.status == TimesheetEntry.Status.REJECTED:
            form.instance.status = TimesheetEntry.Status.PENDING
            form.instance.rejection_reason = ""
        messages.success(self.request, "Timesheet entry updated.")
        return super().form_valid(form)
