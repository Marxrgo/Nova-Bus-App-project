from django.shortcuts import render, get_object_or_404, redirect
from .models import BusSlot, Looptype
from .forms import BusSlotUpdateForm

# Create your views here.

def loop_dashboard(request):
    # Fetch slots for each loop, ordered by slot_number (handled automatically by Meta ordering)
    music_slots = BusSlot.objects.filter(loop =Looptype.MUSIC)
    ib_slots = BusSlot.objects.filter(loop = Looptype.IB)

    context = {
        'music_slots': music_slots,
        'ib_slots': ib_slots,
    }

    return render(request, 'loops/dashboard.html', context)

def update_slot(request, slot_id):
    slot = get_object_or_404(BusSlot, id = slot_id)

    if request.method == 'POST':
        form = BusSlotUpdateForm(request.POST,instance = slot)
        if form.is_valid:
            form.save()
            return redirect('loops:dashboard')
    else:
        form = BusSlotUpdateForm(instance=slot)

    context = {
        'form': form,
        'slot': slot,
    }
    return render(request, 'loops/update_slot.html',context)
        