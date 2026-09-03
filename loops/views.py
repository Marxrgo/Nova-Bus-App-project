from django.shortcuts import render
from .models import BusSlot, Looptype

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