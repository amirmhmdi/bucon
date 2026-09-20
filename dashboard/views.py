import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView

from accounts.models import Profile
from core.models import ContactMessage
from timesheets.models import TimesheetEntry

from .forms import (
    LaborCreateForm,
    LaborUpdateForm,
    PayrollFilterForm,
    ResetPasswordForm,
    TimesheetFilterForm,
)

class ManagerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_manager:
            return HttpResponseForbidden("Manager access only.")
        return super().dispatch(request, *args, **kwargs)

class ManagerDashboardView(ManagerRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            unread_messages=ContactMessage.objects.filter(is_read=False).count(),
            pending_timesheets=TimesheetEntry.objects.filter(
                status=TimesheetEntry.Status.PENDING
            ).count(),
            all_timesheets_count=TimesheetEntry.objects.count(),
            labor_count=Profile.objects.filter(role=Profile.Role.LABOR).count(),
        )
        return context


class PendingTimesheetListView(ManagerRequiredMixin, ListView):
    model = TimesheetEntry
    template_name = "dashboard/pending_timesheets.html"
    context_object_name = "entries"

    def get_queryset(self):
        return TimesheetEntry.objects.filter(status=TimesheetEntry.Status.PENDING)


class AllTimesheetListView(ManagerRequiredMixin, ListView):
    model = TimesheetEntry
    template_name = "dashboard/all_timesheets.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_form(self):
        return TimesheetFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_form()
        queryset = TimesheetEntry.objects.select_related("labor", "labor__profile")

        if not self.filter_form.is_valid():
            return queryset.annotate(
                daily_wage=ExpressionWrapper(
                    F("total_hours") * F("labor__profile__hourly_rate"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ).order_by("-date", "-created_at")

        filters = self.filter_form.cleaned_data
        if filters["labor"]:
            queryset = queryset.filter(labor=filters["labor"])
        if filters["start_date"]:
            queryset = queryset.filter(date__gte=filters["start_date"])
        if filters["end_date"]:
            queryset = queryset.filter(date__lte=filters["end_date"])

        date_order = "date" if filters["sort"] == "oldest" else "-date"
        return queryset.annotate(
            daily_wage=ExpressionWrapper(
                F("total_hours") * F("labor__profile__hourly_rate"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        ).order_by(date_order, "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = getattr(self, "filter_form", self.get_form())
        pagination_query = self.request.GET.copy()
        pagination_query.pop("page", None)
        context["pagination_query"] = pagination_query.urlencode()
        return context


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

# payroll
class PayrollReportView(ManagerRequiredMixin, FormView):
    form_class = PayrollFilterForm
    template_name = "dashboard/payroll_report.html"

    def form_valid(self, form):
        rows = self._build_rows(form.cleaned_data["start_date"], form.cleaned_data["end_date"])
        return render(self.request, self.template_name, {"form": form, "rows": rows})

    def _build_rows(self, start_date, end_date):
        entries = (
            TimesheetEntry.objects.filter(
                status=TimesheetEntry.Status.APPROVED,
                date__range=(start_date, end_date),
            )
            .values("labor__id", "labor__first_name", "labor__last_name", "labor__email")
            .annotate(total_hours=Sum("total_hours"))
        )
        rows = []
        for entry in entries:
            profile = Profile.objects.get(user_id=entry["labor__id"])
            hourly_rate = profile.hourly_rate or 0
            total_hours = entry["total_hours"] or 0
            rows.append(
                {
                    "name": f"{entry['labor__first_name']} {entry['labor__last_name']}".strip()
                    or entry["labor__email"],
                    "total_hours": total_hours,
                    "hourly_rate": hourly_rate,
                    "total_pay": total_hours * hourly_rate,
                }
            )
        return rows


def payroll_csv_export(request):
    if not request.user.profile.is_manager:
        return HttpResponseForbidden()

    form = PayrollFilterForm(request.GET)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=payroll.csv"
    writer = csv.writer(response)
    writer.writerow(["Labor", "Total hours", "Hourly rate", "Total pay"])

    if form.is_valid():
        view = PayrollReportView()
        rows = view._build_rows(form.cleaned_data["start_date"], form.cleaned_data["end_date"])
        for row in rows:
            writer.writerow([row["name"], row["total_hours"], row["hourly_rate"], row["total_pay"]])

    return response
