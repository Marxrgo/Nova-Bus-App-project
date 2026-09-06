from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import BusSlot, Looptype
from .forms import BusSlotUpdateForm
from django.contrib import messages
from django.http import Http404


# Create your views here.

def is_loop_manager(user, loop): #helper function
    return user.is_superuser or user.managed_loop == loop


def loop_dashboard(request): #TODO: change this into 2 dashboards one for music and one for IB
    # Fetch slots for each loop, ordered by slot_number (handled automatically by Meta ordering)
    music_slots = BusSlot.objects.filter(loop =Looptype.MUSIC)
    ib_slots = BusSlot.objects.filter(loop = Looptype.IB)

    context = {
        'music_slots': music_slots,
        'ib_slots': ib_slots,
    }

    return render(request, 'loops/dashboard.html', context)

# Restrict slot modifcation to loggin-in admins
@login_required
def update_slot(request, slot_id):
    slot = get_object_or_404(BusSlot, id = slot_id)

    if not is_loop_manager(request.user, slot.loop):
        raise PermissionDenied

    if request.method == 'POST':
        form = BusSlotUpdateForm(request.POST,instance = slot)
        if form.is_valid():
            form.save()
            return redirect('loops:dashboard')
    else:
        form = BusSlotUpdateForm(instance=slot)

    context = {
        'form': form,
        'slot': slot,
    }
    return render(request, 'loops/update_slot.html',context)

@login_required
def clear_loop(request,loop):
    if loop not in Looptype.values:
        raise Http404("Unknown loop")

    if not is_loop_manager(request.user, loop):
        raise PermissionDenied

    if request.method == 'POST':
        BusSlot.objects.filter(loop = loop).update(bus_number = None) #Filters and remove busnumber thats attached to row
        messages.success(request, f"{dict(Looptype.choices)[loop]} cleared")
        return redirect('loops:dashboard')

    slot_count = BusSlot.objects.filter(loop=loop).count()

    context = {
        'loop': loop,
        'loop_display': dict(Looptype.choices)[loop],
        'slot_count': slot_count,
    }

    return render(request, 'loops/confirm_clear.html', context)
