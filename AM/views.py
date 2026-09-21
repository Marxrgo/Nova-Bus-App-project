from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import staff_required
from .forms import BusStatusForm
from .models import Bus, BusStatus


@staff_required
def staff_dashboard(request):
    today = timezone.localdate()

    #-----
    if request.method == "POST":
        '''Form validation'''
        form = BusStatusForm(request.POST)
        if form.is_valid():
            bus = form.cleaned_data["bus"]
            entered_time = form.cleaned_data["time"]

            defaults = {"is_late": form.cleaned_data["is_late"]}
            if entered_time is not None:
                defaults["arrived_time"] = entered_time

            #Upserts data into database and redirects Admin user to staff dashboard
            BusStatus.objects.update_or_create(bus = bus, date = today, defaults= defaults)
            messages.success(request, f"Bus {bus.number} saved")
            return redirect("AM:staff_dashboard")

    else:
        form = BusStatusForm()

    statuses = BusStatus.objects.filter(date=today).select_related("bus")

    return render(request, "AM/staff_dashboard.html", {
        "form": form,
        "statuses":statuses,
        "today": today,
    })


@staff_required
@require_POST
def mark_arrived(request, status_id):
    status = get_object_or_404(BusStatus, id=status_id)
    status.arrived_time = timezone.localtime().time().replace(second=0, microsecond=0)
    status.save()
    return redirect("AM:staff_dashboard")



@staff_required
@require_POST
def delete_status(request,status_id):
    get_object_or_404(BusStatus, id = status_id).delete()
    return redirect("AM:staff_dashboard")

def bus_status(request, number):

    bus = get_object_or_404(Bus, number = number)

    return render(request, "AM/bus_number.html", {
        "bus": bus,
        "status": BusStatus.status_for(bus),
        "today": timezone.localdate()
    })





