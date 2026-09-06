from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from loops.views import is_loop_manager
from loops.models import BusSlot
from .models import LateReport, Announcement
from .forms import LateReportForm, AnnouncementForm


def _active_reports_and_announcements():
    reports = [r for r in LateReport.objects.select_related("slot") if r.is_active]
    announcements = [a for a in Announcement.objects.all() if a.is_active]
    return reports, announcements


def late_dashboard(request):
    """Public dashboard. Also serves as the destination for accounts:teacher_access,
    since teacher-key entry has no dedicated feature of its own yet."""
    reports, announcements = _active_reports_and_announcements()
    return render(request, "latebus/late_dashboard.html", {
        "reports": reports,
        "announcements": announcements,
        "via_teacher_access": request.session.get("teacher_access", False),
    })


@login_required
def create_report(request):
    if request.method == "POST":
        form = LateReportForm(request.POST)
        if form.is_valid():
            slot = form.cleaned_data["slot"]
            if not is_loop_manager(request.user, slot.loop):
                raise PermissionDenied
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            return redirect("latebus:dashboard")
    else:
        form = LateReportForm()
        if not request.user.is_superuser and request.user.managed_loop:
            form.fields["slot"].queryset = BusSlot.objects.filter(loop=request.user.managed_loop)
    return render(request, "latebus/report_form.html", {"form": form})


@login_required
def resolve_report(request, report_id):
    report = get_object_or_404(LateReport, id=report_id)
    if not is_loop_manager(request.user, report.slot.loop):
        raise PermissionDenied
    report.resolve()
    return redirect("latebus:dashboard")


@login_required
def create_announcement(request):
    if not (request.user.is_superuser or request.user.managed_loop):
        raise PermissionDenied
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
loop = form.cleaned_data.get("loop")
if loop:
    if not is_loop_manager(request.user, loop):
        raise PermissionDenied
elif not request.user.is_superuser:
    # Blank loop means "system-wide" — only superusers may post those.
    raise PermissionDenied
            ann = form.save(commit=False)
            ann.created_by = request.user
            ann.save()
            return redirect("latebus:dashboard")
    else:
        form = AnnouncementForm()
    return render(request, "latebus/announcement_form.html", {"form": form})


@login_required
def resolve_announcement(request, announcement_id):
    ann = get_object_or_404(Announcement, id=announcement_id)
    if ann.loop and not is_loop_manager(request.user, ann.loop):
        raise PermissionDenied
    if not ann.loop and not request.user.is_superuser:
        raise PermissionDenied
    ann.resolve()
    return redirect("latebus:dashboard")
