from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView

from core.models import ContactMessage
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


#contact
class ContactMessageListView(ManagerRequiredMixin, ListView):
    model = ContactMessage
    template_name = "dashboard/contact_messages.html"
    context_object_name = "contact_messages"


def mark_message_read(request, pk):
    if not request.user.profile.is_manager:
        return HttpResponseForbidden()
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save(update_fields=["is_read"])
    return redirect("dashboard:contact_messages")

#labor account managment
class LaborListView(ManagerRequiredMixin, ListView):
    model = Profile
    template_name = "dashboard/labor_list.html"
    context_object_name = "labors"

    def get_queryset(self):
        return Profile.objects.filter(role=Profile.Role.LABOR).select_related("user")


class LaborCreateView(ManagerRequiredMixin, FormView):
    form_class = LaborCreateForm
    template_name = "dashboard/labor_form.html"
    success_url = reverse_lazy("dashboard:labor_list")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Labor account created.")
        return super().form_valid(form)


class LaborUpdateView(ManagerRequiredMixin, UpdateView):
    model = Profile
    form_class = LaborUpdateForm
    template_name = "dashboard/labor_form.html"
    success_url = reverse_lazy("dashboard:labor_list")

    def get_queryset(self):
        return Profile.objects.filter(role=Profile.Role.LABOR)


def reset_labor_password(request, pk):
    if not request.user.profile.is_manager:
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=pk, role=Profile.Role.LABOR)
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            profile.user.set_password(form.cleaned_data["temporary_password"])
            profile.user.save()
            profile.must_change_password = True
            profile.save(update_fields=["must_change_password"])
            messages.success(request, f"Password reset for {profile.user}.")
            return redirect("dashboard:labor_list")
    else:
        form = ResetPasswordForm()
    return render(request, "dashboard/reset_password.html", {"form": form, "profile": profile})