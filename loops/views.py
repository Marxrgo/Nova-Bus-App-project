from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import BusSlot, Looptype
from .forms import BusSlotUpdateForm


# Create your views here.

def is_loop_manager(user, loop):
    return user.is_superuser or user.managed_loop == loop



def loop_dashboard(request):
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
    