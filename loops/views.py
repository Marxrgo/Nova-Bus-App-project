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

def loop_index(request):
    return render(request, 'loops/index.html')


def loop_dashboard(request, loop): #renders dash for either loop
    if loop not in Looptype.values:
        raise Http404("Unknown loop")

    slots = BusSlot.objects.filter(loop = loop) #filters for either bus or ib loop
    template_name = f'loops/{loop.lower()}_loop.html'  #loads corrent html/css accoding to each loop

    context = {
        'loop': loop,
        'loop_display': dict(Looptype.choices)[loop],
        'slots': slots
    }

    return render(request, template_name, context)

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
            return redirect('loops:loop_dashboard', loop = slot.loop)
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
        return redirect('loops:loop_dashboard', loop = loop)

    slot_count = BusSlot.objects.filter(loop=loop).count()

    context = {
        'loop': loop,
        'loop_display': dict(Looptype.choices)[loop],
        'slot_count': slot_count,
    }

    return render(request, 'loops/confirm_clear.html', context)
