from django import forms
from .models import BusSlot

class BusSlotUpdateForm(forms.ModelForm):
    class Meta:
        model = BusSlot
        fields = ['bus_number']
        widgets = {
            'bus_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Bus #',
                'min': '1',
            }),
        }